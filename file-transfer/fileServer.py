#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    if os.fork() == 0:      # child becomes server
        data = conn.recv(1024).decode()
        delim = data.index(":")
        msg_length = int(data[:delim])
        file_name = data[delim + 1:msg_length + delim + 1]
        data = data[msg_length + delim + 1:]
        file_descriptor = os.open(file_name, os.O_CREAT | os.O_WRONLY)
        
        full_msg = ""
        msg = ""
        new_msg = True
        while data:
            if new_msg:
                delim = data.index(":")
                msg_length = int(data[:delim])
            
                msg = data[delim + 1:]
                new_msg = False
            else:
                msg = data

            full_msg += msg
            msg_length -= len(msg)
            data = conn.recv(1024).decode()
            
            if msg_length == 0:
                os.write(file_descriptor, full_msg.encode())
                break
        
        conn.shutdown(socket.SHUT_WR)



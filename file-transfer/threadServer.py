#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from threading import Thread, Lock

def checkTransfer(fileName):
    global inTransfer
    
    canTransfer = False
    threadLock.acquire()
    if fileName in inTransfer:
        canTransfer = False
    else:
        canTransfer = True
        inTransfer.add(fileName)
    threadLock.release()
    return canTransfer

def serverThread(conn):
    global inTransfer
    data = conn.recv(1024).decode()
    delim = data.index(":")
    msg_length = int(data[:delim])
    rs = data[delim + 1]
    file_name = data[delim + 2:msg_length + delim + 1]

    valid_transfer = checkTransfer(file_name)
    
    if not valid_transfer:
        conn.send("File transfer failed!".encode())
    elif rs == "s":
        file_descriptor = os.open(file_name, os.O_CREAT | os.O_WRONLY)
        data = data[msg_length + delim + 1:]
        delim = data.index(":")
        msg_length = int(data[:delim])
        data = data[delim + 1:]
        full_msg = ""
        while data:
            full_msg += data
            msg_length -= len(data)
            data = conn.recv(1024).decode()
            
            if msg_length == 0:
                os.write(file_descriptor, full_msg.encode())
                break
        
        inTransfer.remove(file_name)
    
    else:
        file_descriptor = os.open(file_name, os.O_RDONLY)
        file_size = os.path.getsize(file_name)
        chunk = os.read(file_descriptor, 1024)
        conn.send("{0}:{1}".format(file_size, chunk.decode()).encode())
    
        while True:
            chunk = os.read(file_descriptor, 1024)
            if not chunk:
                break
            else:
                conn.send(chunk)
        
        inTransfer.remove(file_name)
    
    conn.shutdown(socket.SHUT_WR)


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

threadLock = Lock()
inTransfer = set()
while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    
    new_thread = Thread(target=serverThread, args=(conn,))
    new_thread.start()


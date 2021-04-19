#! /usr/bin/env python3

import sys, os, socket
from time import time, sleep
from threading import Thread, enumerate, Lock

global count
count = 0
global countLock
countLock = Lock()
inTransfer = set()
threadNum = 0

class Worker(Thread):
    def __init__(self, conn):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum)
        threadNum += 1
        self.conn = conn

    def check_transfer(self, file_name):
        global inTransfer
        global countLock
        countLock.acquire()
        if file_name not in inTransfer:
            inTransfer.add(file_name)
            countLock.release()
            return True
        countLock.release()
        return False
    
    def run(self):
        global inTransfer
        data = self.conn.recv(1024).decode()
        delim = data.index(":")
        msg_length = int(data[:delim])
        rs = data[delim + 1]
        file_name = data[delim + 2:msg_length + delim + 1]
    
        if not self.check_transfer(file_name):
            self.conn.send("File transfer failed!".encode())
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
                data = self.conn.recv(1024).decode()
            
                if msg_length == 0:
                    os.write(file_descriptor, full_msg.encode())
                    break
            inTransfer.remove(file_name)
        else:
            file_descriptor = os.open(file_name, os.O_RDONLY)
            file_size = os.path.getsize(file_name)
            chunk = os.read(file_descriptor, 1024)
            self.conn.send("{0}:{1}".format(file_size, chunk.decode()).encode())
            while True:
                chunk = os.read(file_descriptor, 1024)
                if not chunk:
                    break
                else:
                    self.conn.send(chunk)
            inTransfer.remove(file_name)
        self.conn.shutdown(socket.SHUT_WR)

    

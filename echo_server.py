#!/usr/bin/python3
# usage python3 echoTcpServer.py [bind IP]  [bind PORT]

import socket
import sys
import string
import random

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
#ip=socket.gethostbyname('localhost')
ip = "0.0.0.0"
port=3303
size = 1024
backlog = 1
address=(ip,port) 
sock.bind(address)
# Listen for incoming connections
sock.listen(backlog)
connections = []
while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        connection.setblocking(False)
        connections.append(connection)
        print('connection from', client_address)
        message = connection.recv(size)
        if message:
            print("Message Received!: %s" %message)
            connection.send(message)
            print("sent %s bytes back to %s" % (message,client_address))
        connection.close()
        

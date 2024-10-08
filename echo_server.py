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
backlog = 2
address=(ip,port) 
sock.bind(address)
# Listen for incoming connections
sock.listen(backlog)
connections = []
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    connections.append(connection)
    print('connection from', client_address)
    for connection in connections:
        try:
            message = connection.recv(size)
            print(message)
        except BlockingIOError:
            continue
        for connection in connections:
            connection.send(message)

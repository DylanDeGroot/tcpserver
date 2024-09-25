#!/usr/bin/python3
# usage python3 echoTcpServer.py [bind IP]  [bind PORT]

import socket
import sys
import string
import random

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
ip=socket.gethostbyname("13.56.253.227")
port=3303
size = 1024
backlog = 2
address=(ip,port) 
sock.bind(address)
# Listen for incoming connections
sock.listen(backlog)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(size)
            if not data:
                break
            connection.sendall(data)
    finally:
        # Clean up the connection
        connection.close()
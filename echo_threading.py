import socket
import thread

class SocketServer(socket.socket):
    clients = []

    def __init__(self):
        socket.socket.__init__(self)
        #To silence- address occupied!!
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(('0.0.0.0', 3030))
        self.listen(5)

    def run(self):
        print("Server started")
        try:
            self.accept_clients()
        except Exception as ex:
            print ex
        finally:
            print("Server closed")
            for client in self.clients:
                client.close()
            self.close()

    def accept_clients(self):
        while 1:
            (clientsocket, address) = self.accept()
            #Adding client to clients list
            self.clients.append(clientsocket)
            #Client Connected
            self.onopen(clientsocket)
            #Receiving data from client
            thread.start_new_thread(self.recieve, (clientsocket,))

    def recieve(self, client):
        while 1:
            data = client.recv(1024)
            if data == '':
                break
            #Message Received
            self.onmessage(client, data)
        #Removing client from clients list
        self.clients.remove(client)
        #Client Disconnected
        self.onclose(client)
        #Closing connection with client
        client.close()
        #Closing thread
        thread.exit()
        print(self.clients)

    def broadcast(self, message):
        #Sending message to all clients
        for client in self.clients:
            client.send(message)

    def onopen(self, client):
        pass

    def onmessage(self, client, message):
        pass

    def onclose(self, client):
        pass
class BasicChatServer(SocketServer):

    def __init__(self):
        SocketServer.__init__(self)

    def onmessage(self, client, message):
        print("Client Sent Message")
        #Sending message to all clients
        self.broadcast(message)

    def onopen(self, client):
        print("Client Connected")

    def onclose(self, client):
        print("Client Disconnected")

def main():
    server = BasicChatServer()
    server.run()

if __name__ == "__main__":
    main()

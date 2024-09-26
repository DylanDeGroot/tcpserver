import socket
import _thread
import time

class SocketServer(socket.socket):
    clients = []
    PCs = []
    lights = []

    def __init__(self):
        socket.socket.__init__(self)
        #To silence- address occupied!!
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(('0.0.0.0', 3303))
        self.listen(5)

    def run(self):
        print("Server started")
        try:
            self.accept_clients()
        except Exception as ex:
            print(ex)
        finally:
            print("Server closed")
            for client in self.clients:
                client.close()
            self.close()

    def accept_clients(self):
        while 1:
            (clientsocket, address) = self.accept()
            time.sleep(5)
            #Ask for identification
            clientsocket.send(b'Input SN if light or PC')
            #Wait for response
            while 1:
                data = clientsocket.recv(1024)
                #msg = data.decode('utf-8')
                if not data:
                    break
                if b'PC' in data:
                    self.PCs.append(clientsocket)
                    client_type = 'PC'
                if data.startswith(b'F'):
                    self.lights.append(clientsocket)
                    client_type = 'LIGHT'
            #Adding client to clients list
            self.clients.append(clientsocket)
            #Client Connected
            self.onopen(clientsocket,client_type)
            #Receiving data from client
            _thread.start_new_thread(self.recieve, (clientsocket,), client_type)

    def recieve(self, client, client_type):
        while 1:
            data = client.recv(1024)
            msg = data.decode('utf-8')
            if not data:
                break
            #Message Received
            self.onmessage(client, data, client_type)
        #Removing client from clients list
        self.clients.remove(client)
        if 'PC' in client_type:
            self.PCs.remove(client)
        if 'LIGHT' in client_type:
            self.lights.remove(client)
        #Client Disconnected
        self.onclose(client)
        #Closing connection with client
        client.close()
        #Closing thread
        _thread.exit()
        print(self.clients)

    def broadcast(self, message, client_type):
        if 'PC' in client_type:
            for light in self.lights:
                light.send(message)
        if 'LIGHT' in client_type:
            for PC in self.PCs:
                PC.send(message)
        #Sending message to all clients
        #for client in self.clients:
            #client.send(message)

    def onopen(self, client,client_type):
        pass

    def onmessage(self, client, message):
        pass

    def onclose(self, client):
        pass
class BasicChatServer(SocketServer):

    def __init__(self):
        SocketServer.__init__(self)

    def onmessage(self, client, message, client_type):
        if 'PC' in client_type:
            print("PC Sent Message")
        if 'LIGHT' in client_type:
            print("LIGHT Sent Message")
        #broadcast message to
        self.broadcast(message, client_type)

    def onopen(self, client, client_type):
        if 'PC' in client_type:
            print("PC Connected")
        if 'LIGHT' in client_type:
            print("LIGHT Connected")
    def onclose(self, client, client_type):
        if 'PC' in client_type:
            print("PC Disconnected")
        if 'LIGHT' in client_type:
            print("LIGHT Disconnected")

def main():
    server = BasicChatServer()
    server.run()

if __name__ == "__main__":
    main()

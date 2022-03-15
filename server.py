import threading
import socket
import os

host = '0.0.0.0'
#host = '127.0.0.1'
#port = 14150
port =  socket.htons(0)
#host = socket.htonl(socket.INADDR_ANY)
#port = int(os.environ.get('PORT'))

#setup server, then link host port info
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#client lists
clients = []
usernames = []

#sends message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


#handles clients
def handle(client):
    #when client no longer connected, the error will be thrown
    while True:
        try:
            #packet of message at 1024
            message = client.recv(1024)
            broadcast(message)
            
        except:
            #removes client from lists
            i = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[i]
            broadcast(f'{username} has left the chat.'.encode('ascii'))
            usernames.remove(username)
            break

#receiving new clients
def receive():
    while True:
        #upon joining
        client, address = server.accept()
        print(f"{str(address)} has connected")

        # sends keyphrase to client
        client.send('Enter Username:'.encode('ascii'))
        # get username from client
        username = client.recv(1024).decode('ascii')
        clients.append(client)
        usernames.append(username)
        print(f'New client {username}')

        #send message of new client
        broadcast(f'{username} has joined the chat.'.encode('ascii'))
        client.send('Successfully connected to server.'.encode('ascii'))

        #threading to manage multiple users
        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

print("server is listening")
print(port)
receive()
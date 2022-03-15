import socket
import threading
import server

username = input("Enter Username: ")

#setup client then connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server.host, server.port))

def receive():
    while True:
        try:
            # receives keyphrase from server
            message = client.recv(1024).decode('ascii')

            # sends username to server
            if message == 'Enter Username:':
                client.send(username.encode('ascii'))
            else:
                print(message)

        except:
            print("An error occurred")
            client.close()
            break

def chat():
    while True:
        # user chats to server using this
        message = f'{username}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=chat)
write_thread.start()
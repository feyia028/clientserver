import socket #Used for internet connections
import threading #Allows many functions to be executed at once

HOST = '127.0.0.1' #General local host IP address 
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet and TCP socket
server.bind((HOST, PORT)) #Binds to a tuple

server.listen() #Listens for potential connections when the script is ran

clients = []
displaynames = []

def broadcast(message):
        for client in clients:
                client.send(message) #Function which allows the server to send messages to every client connected to the server

def handle(client): #Client is a parameter so we can run a thread
        while True:
                try:
                        message = client.recv(1024) #Receives the message of a client in a buffer size of 1024 bytes at a time
                        broadcast(message)
                except:
                        index = clients.index(client) #Searches for the index of the client
                        clients.remove(client) #Removes the client off the array
                        client.close()
                        displayname = displaynames[index] #Searches for the displayname index of the client
                        broadcast(f'{displayname} has left the chat'.encode('utf-8')) #Shows all connected users that the client has left
                        displaynames.remove(displayname) #Removes the client's display name off the array
                        break

def receive():
        while True:
                client, address = server.accept() #Accepts new connections
                print(f"Connected with {str(address)}!") #Shows the host and port number the client has connected with

                client.send("Please enter your display name".encode('utf-8')) #Asks the client for a displayname
                displayname = client.recv(1024).decode('utf-8') #Receives the nickname in a buffer size of 1024 bytes at a time
                
                displaynames.append(displayname) #Appends the displayname to the displayname list
                clients.append(client) #Appends the client to the client list

                print(f"Your display name is {displayname}") #Shows the cloient their displayname
                broadcast(f"{displayname} is online right now!\n".encode('utf-8')) #Shows all the other clients the new client
                client.send("Connected to the server".encode('utf-8')) #Indicates to the client that they are connected.

                thread = threading.Thread(target=handle, args=(client,)) #For each client which has a connection, this thread is ran
                thread.start()                                           #There is a comma after client so that it is saved as a tuple.

print("Server in full effect!") #Indicates the server is working
receive()  


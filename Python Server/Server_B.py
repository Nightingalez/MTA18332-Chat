from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

serverHost = ''
serverPort = 33000
bufferSize = 1024
addr = (serverHost, serverPort)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)

def accept_incoming_connections():

    while True:
        client, client_addresses = server.accept()
        print("%s:%s has connected." % client_addresses)
        client.send(bytes("Greetings from the cave!" + "Now type your name and press enter!", "utf8"))

        addresses[client] = client_addresses
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client): #Takes the client's socket as an argument
    name = client.recv(bufferSize).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(bufferSize)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__== "__main__":
    server.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()




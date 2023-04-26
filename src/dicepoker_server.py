import socket
import threading
import random

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# bind the socket to a public host, and a well-known port
server_socket.bind((host, 12345))

# set the server to listen for incoming connections
server_socket.listen(2)
print("Waiting for clients to connect...")

# store client sockets and addresses
clients = []
addresses = []

# function to roll a six-sided dice


def roll_dice():
    return random.randint(1, 6)

# roll 5 public dice and return as string


def roll_public_dice():
    return " ".join([str(roll_dice()) for _ in range(5)])

# roll 2 private dice and return as string


def roll_private_dice():
    return " ".join([str(roll_dice()) for _ in range(2)])

# function to handle a client connection


def handle_client(client_socket, address):
    # send private rolls to the client
    client_socket.send(f"Your private rolls: {roll_private_dice()}\n".encode())

    # send public rolls to both clients
    client_socket.send(f"Public rolls: {public_rolls}\n".encode())

    # loop until client disconnects
    while True:
        try:
            # receive data from client
            data = client_socket.recv(1024).decode()

            # if client disconnects, break loop
            if not data:
                break

            # otherwise, send back the data
            client_socket.send(f"You sent: {data}".encode())
        except:
            # if an error occurs, break loop
            break

    # close the client socket
    client_socket.close()


public_rolls = roll_public_dice()
# loop indefinitely to handle client connections
while True:
    # accept a new client connection
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} established.")

    # add client socket and address to lists
    clients.append(client_socket)
    addresses.append(address)

    # start a new thread to handle the client connection
    threading.Thread(target=handle_client, args=(
        client_socket, address)).start()

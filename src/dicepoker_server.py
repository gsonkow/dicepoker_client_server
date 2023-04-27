import socket
import threading
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

# bind the socket to a public host, and a well-known port
server_socket.bind((host, 12345))

# set the server to listen for incoming connections
server_socket.listen(2)
print("Waiting for clients to connect...")

clients = []
addresses = []


def roll_dice():
    return random.randint(1, 6)


def roll_public_dice():
    return " ".join([str(roll_dice()) for _ in range(5)])


def roll_private_dice():
    return " ".join([str(roll_dice()) for _ in range(2)])


def calc_value(private_dice, public_dice):
    dice = []
    value = 0
    for die in private_dice + public_dice:
        if die == "1":
            dice[0] += 1
        elif die == "2":
            dice[1] += 1
        elif die == "3":
            dice[2] += 1
        elif die == "4":
            dice[3] += 1
        elif die == "5":
            dice[4] += 1
        elif die == "6":
            dice[5] += 1
    for score in dice:
        if score >= 3 and value < score - 2:
            value = score - 2

    return value


def handle_client(client_socket, address):
    private_rolls = roll_private_dice()
    client_socket.send(f"Your private rolls: {private_rolls}\n".encode())

    client_socket.send(f"Public rolls: {public_rolls}\n".encode())

    client_socket.send(
        f"Your hand's value is: {calc_value(private_rolls, public_rolls)}\n".encode())

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
while True:
    # accept a new client connection
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} established.")

    clients.append(client_socket)
    addresses.append(address)

    threading.Thread(target=handle_client, args=(
        client_socket, address)).start()

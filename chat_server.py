import os.path
import socket
import threading
from math import ceil

CLIENT_COUNTER = 1
CHAT_CLIENTS = {}
USERNAMES = []
CHAT_ROOMS = {'room1': [], 'room2': [], 'room3': [], }


def print_client():
    global CHAT_CLIENTS
    for client_name in CHAT_CLIENTS.keys():
        print(f'{client_name} is online')


def chat_session(chat_client_socket, client_name):
    while True:
        try:
            data = chat_client_socket.recv(1024)
        except (Exception,):
            global CLIENT_COUNTER
            print(f'{client_name} Disconnected')
            CHAT_CLIENTS.pop(client_name)
            check_tuple = check_room(chat_client_socket)
            if check_tuple[0]:
                CHAT_ROOMS[check_tuple[1]].remove(chat_client_socket)
            chat_client_socket.close()
            CLIENT_COUNTER -= 1

            print(CHAT_CLIENTS)
            break
        else:

            if data.decode() == '-show_online':
                print_client()
            elif data.decode().startswith('-pr'):
                private_message(CHAT_CLIENTS, data, client_name)
            elif data.decode().startswith('-goto'):
                chat_rooms(data, chat_client_socket)
            elif data.decode().startswith('-file'):
                get_file(chat_client_socket, data.decode())
            else:
                broadcast_message(CHAT_CLIENTS, data, client_name, chat_client_socket)


def private_message(clients, message, sender):
    to_client_name = message.decode().split('-pr ')[1].split()[0]
    for client in clients.values():
        if list(clients.keys())[list(clients.values()).index(client)] == to_client_name:
            formatted_message = str(message.decode().split('-pr ')[1].split()[1])
            formatted_message = f'{sender}: {formatted_message}'
            client.send(bytes(formatted_message, "utf-8"))


def chat_rooms(message, room_client_socket):
    global CHAT_ROOMS
    room_name = message.decode().split()[1]
    check_tuple = check_room(room_client_socket)
    if check_tuple[1] != room_name:
        CHAT_ROOMS[check_tuple[1]].remove(room_client_socket)
        CHAT_ROOMS[room_name].append(room_client_socket)
    elif check_tuple[1] == room_name:
        print(f'Already in {room_name}')


def check_room(room_client_socket):
    room_name = 0
    for clients in CHAT_ROOMS.values():
        room_name += 1
        for client in clients:
            if client == room_client_socket:
                room_name = str(f'room{room_name}')
                return True, room_name
    return False,


def get_file(client_socket_file, file_message):
    client_socket_file.send(bytes(file_message, "utf-8"))
    file_message = client_socket_file.recv(1024).decode()
    properties = file_message.split()
    file_name = os.path.basename(properties[1])
    send_to = f'{os.path.abspath(os.getcwd())}\\Files\\{file_name}'
    try:
        size = int(properties[2])
        loops_counter = int(ceil(size / 1024))
        with open(send_to, 'wb') as file:
            for x in range(0, loops_counter):
                data = client_socket_file.recv(1024)
                file.write(data)
            else:
                print('File sent successfully')
    except(Exception,):
        print("File not exist")


def broadcast_message(clients, message, sender, chat_client):
    global CHAT_ROOMS
    check_tuple = check_room(chat_client)
    for client in CHAT_ROOMS[check_tuple[1]]:
        if list(clients.keys())[list(clients.values()).index(client)] != sender:
            client.send(bytes(str(f'{sender}: {message.decode()}'), "utf-8"))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('###.###.###.###', 9999)) # IP PLACEHOLDER
server_socket.listen(5)

while True:
    print('server is listening...')
    client_socket, address = server_socket.accept()
    username = client_socket.recv(1024).decode()
    USERNAMES.append(username)
    print(f'connection {address} has been establish')
    CHAT_CLIENTS.update({username: client_socket})
    CHAT_ROOMS['room1'].append(client_socket)
    print(CHAT_CLIENTS)
    session_thread = threading.Thread(target=chat_session, args=(client_socket, username))
    session_thread.start()
    CLIENT_COUNTER += 1

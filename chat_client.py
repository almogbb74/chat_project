import os
import threading
import socket


def receive_broadcast(broad_socket):
    while True:
        message = broad_socket.recv(1024)
        if message.decode().startswith('-file'):
            send_file(broad_socket, message.decode())
        else:
            print(message.decode())


def send_file(client_socket_file, message):
    image_path = message.split()[1]
    try:
        message = f'-file {image_path} {os.path.getsize(image_path)}'
        client_socket_file.send(bytes(message, "utf-8"))
        with open(image_path, 'rb') as file:
            data = file.read(1024)
            print('Data being transferred...')
            while data:
                client_socket_file.send(data)
                data = file.read(1024)
            print('Data transferred successfully')
    except(Exception,):
        print("Couldn't find specified file")


def chat_input():
    while True:
        cmd = input()
        if cmd == 'bye':
            client_socket.close()
            break
        else:
            client_socket.send(bytes(cmd, "utf-8"))


username = input("Enter name:")
with open('users.txt') as f:
    lines = f.readlines()
    lines = [line.rstrip() for line in lines]

for line in lines:
    if line == username:
        print(f'Welcome back, {username}')
        break
else:
    if os.path.getsize('users.txt') > 0:
        with open('users.txt', 'a') as f:
            f.write(f'\n{username}')
    else:
        with open('users.txt', 'w') as f:
            f.write(username)
    print(f'Hello {username}!')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.178', 9999))
client_socket.send(bytes(username, "utf-8"))

print("Welcome to Whatsapp 2.0! Have fun ;)\n"
      "-For private messages start message with -pr [username] [message]\n"
      "-To enter a chat room (default room is room1) type -goto [room1, room2, room3]\n"
      "-To send a file over the chat (to the server) use: -file [path]")

rec_broadcast_thread = threading.Thread(target=receive_broadcast, args=[client_socket])
rec_broadcast_thread.start()

chat_input_thread = threading.Thread(target=chat_input)
chat_input_thread.start()

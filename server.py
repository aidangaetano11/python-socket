import socket
from sys import stdout
import threading
import os


def handle_client(client_socket):
    def send_messages():
        while True:
            try:
                message = input("Server: ")
                if message.startswith("SEND"):
                    file_path = message.split(" ", 1)[1]
                    if os.path.exists(file_path):
                        file_name = os.path.basename(file_path)
                        client_socket.send(f"FILE_NAME:{file_name}".encode())

                        with open(file_path,"rb") as file:
                            while(chunk := file.read(1024)):
                                client_socket.send(chunk)
                        client_socket.send(b"END_OF_FILE")
                        print(f"Sent {file_name} to client.")
                    else:
                        print(f"File {file_path} not found.")
                else:
                    client_socket.send(message.encode())
            except:
                break

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message.startswith("FILE:"):
                    file_name = message.split(":")[1]
                    with open(f"received_{file_name}", "wb") as file:
                        while True:
                            chunk = client_socket.recv(1024)
                            if chunk == b"END_OF_FILE":
                                break
                            file.write(chunk)
                    print(f"Received file {file_name} from client")
                else:
                    print(f"Client: {message}")
            except:
                break

    send_thread = threading.Thread(target=send_messages)
    receive_thread = threading.Thread(target=receive_messages)

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5)

while True:
    client, address = server.accept()
    print(f"Received connection from {address}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
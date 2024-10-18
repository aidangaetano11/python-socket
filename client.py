import socket
from sys import stdout
import threading
import os

def send_messages(client_socket):
    while True:
        try:
            message = input("Client: ")
            if message.startswith("SEND"):
                file_path = message.split(" ", 1)[1]
                if os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    file_size = os.path.getsize(file_path)
                    client_socket.send(f"FILE_NAME:{file_name}:{file_size}".encode())

                    with open(file_path,"rb") as file:
                        while(chunk := file.read(1024)):
                            client_socket.send(chunk)
                    print(f"Sent {file_name} to server.")
                else:
                    print(f"File {file_path} not found.")
            else:
                client_socket.send(message.encode())
        except Exception as e:
            print(f"Connection closed due to error: {e}.")
            client_socket.close()
            break

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith("FILE_NAME:"):
                file_info = message.split(":")
                file_name = file_info[1]
                file_size = int(file_info[2])
                received_size = 0
                print(f"Receiving file: {file_name}, Size: {file_size} bytes")

                with open(f"client_receive_files/received_{file_name}", "wb") as file:
                    while received_size < file_size:
                        chunk = client_socket.recv(min(1024, file_size - received_size))
                        file.write(chunk)
                        received_size += len(chunk)
                        
                print(f"Received file {file_name} from server.")
            else:
                stdout.write(f"\nServer: {message}\nClient: ")
                stdout.flush()
        except Exception as e:
            print(f"Connection Closed due to error: {e}.")
            client_socket.close()
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.200', 9999))

send_thread = threading.Thread(target=send_messages, args=(client,))
receive_thread = threading.Thread(target=receive_messages, args=(client,))

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

client.close()
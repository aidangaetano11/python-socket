import socket
from sys import stdout
import threading
import os


def handle_client(client_socket):
    # Server sending messages to client
    def send_messages():
        while True:
            try:
                message = input("Server: ")
                # Sending a file
                if message.startswith("SEND"):
                    file_path = message.split(" ", 1)[1]
                    if os.path.exists(file_path):
                        file_name = os.path.basename(file_path)
                        file_size = os.path.getsize(file_path)
                        client_socket.send(f"FILE_NAME:{file_name}:{file_size}".encode())

                        # Read file
                        with open(file_path,"rb") as file:
                            while(chunk := file.read(1024)):
                                client_socket.send(chunk)

                        print(f"Sent {file_name} to client.")
                    else:
                        print(f"File {file_path} not found.")
                # Sending a text message
                else:
                    client_socket.send(message.encode())
            except Exception as e:
                print(f"Error in sending: {e}")
                break

    # Server receiving messages from client
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode()
                # Receiving a file
                if message.startswith("FILE_NAME:"):
                    file_info = message.split(":")
                    file_name = file_info[1]
                    file_size = int(file_info[2])
                    received_size= 0
                    print(f"Receiving file: {file_name}, Size: {file_size} bytes")


                    with open(f"server_received_files/received_{file_name}", "wb") as file:
                        while received_size < file_size:
                            chunk = client_socket.recv(min(1024, file_size - received_size))
                            file.write(chunk)
                            received_size += len(chunk)
                    print(f"Received file {file_name} from client.")
                #Receiving a message
                else:
                    stdout.write(f"\nClient: {message}\nServer: ")
                    stdout.flush()
            except Exception as e:
                print(f"Error in receiving: {e}")
                break

    # Using threads to do multiple operations at a time
    send_thread = threading.Thread(target=send_messages)
    receive_thread = threading.Thread(target=receive_messages)

    send_thread.start()
    receive_thread.start()

    # Make sure the threads complete before continuing
    send_thread.join()
    receive_thread.join()
    
    client_socket.close()

# Create new socket using IPv4 and TCP protocol at port 8888
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8888))
# Allows up to 5 clients to connect at once
server.listen(5)
print("Server listening from port 8888...")

# Wait for client to connect and create threading for client
while True:
    client, address = server.accept()
    print(f"Received connection from {address}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
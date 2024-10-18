import socket
from sys import stdout
import threading


def handle_client(client_socket):
    def send_messages():
        while True:
            try:
                message = input("Server: ")
                client_socket.send(message.encode())
            except:
                break

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                stdout.write(f"\nClient: {message}\nServer: ")
                stdout.flush()
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
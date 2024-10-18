import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Client: {message}")

            reply = input("Server: ")
            client_socket.send(reply.encode())
        except:
            break
    
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))

server.listen(5)

while True:
    client, address = server.accept()
    print(f"Received connection from {address}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
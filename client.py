import socket
from sys import stdout
import threading

def send_messages(client_socket):
    while True:
        try:
            message = input("Client: ")
            client_socket.send(message.encode())
        except:
            print("Connection closed.")
            client_socket.close()
            break

def receive_messages(client_socket):
    while True:
        try:
            reply = client_socket.recv(1024).decode()
            if not reply:
                break
            stdout.write(f"\nServer: {reply}\nClient: ")
            stdout.flush()
        except:
            print("Connection Closed.")
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
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.200', 9999))

client.send("Hello From Client".encode())
print(client.recv(1024))
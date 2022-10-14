import socket

target = "0.0.0.0"
port = 9998

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target, port))

client.send(b"MAMONES FC jeje\r\n\r\n")

response = client.recv(4096)

print(response.decode())
client.close()
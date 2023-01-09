import socket
import threading
import sys
import subprocess

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
		client_socket.send("BHP:#> ".encode('utf-8'))
		
		cmd_buffer = b''
		# recibimos hasta un Enter
		while b"\n" not in cmd_buffer:
			cmd_buffer += client_socket.recv(1024)

		# enviamos los resultados del comando
		response = run_command(cmd_buffer.decode())
		client_socket.send(response)

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

	if len(sys.argv) < 2:
		print("NOT ENOUGH ARGUMENTS")
		print("Usage:")
		print("python listen.py IP_ADDRESS PORT")
		sys.exit(0)
	target = sys.argv[1]
	port = int(sys.argv[2])
	server_loop()

main()
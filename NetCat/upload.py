import sys
import socket
import getopt
import threading
import subprocess

target = ""
upload_destination = ""
port = 0


def client_handler(client_socket):
	global upload

	# leemos todos los bytes y escribimos al destino
	file_buffer = ""

	# seguir leyendo hasta que se agote
	while True:
		data = client_socket.recv(1024)

		if not data:
			break
		else:
			file_buffer += data

	# tomamos los bytes e intentamos escribirlos
	try:
		file_descriptor = open(upload_destination, "wb")
		file_descriptor.write(file_buffer.encode('utf-8'))
		file_descriptor.close()

		# notificamos que la escritura fue exitosa
		client_socket.send("Archivo guardado en %s\r\n" % upload_destination)
	except OSError:
		client_socket.send("Error al guardar archivo\r\n")		


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
	global upload_destination

	if len(sys.argv) < 3:
		print("NOT ENOUGH ARGUMENTS")
		print("Usage:")
		print("python listen.py IP_ADDRESS PORT")
		sys.exit(0)
	target = sys.argv[1]
	port = int(sys.argv[2])
	upload_destination = sys.argv[3]
	server_loop()

main()
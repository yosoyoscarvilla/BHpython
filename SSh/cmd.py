import paramiko

def command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    #paramiko soporta auth por llaves, ademas de password
    # esta funcion setea la politica al conectarse a serv
    #sin host key conocido
    #AutoAddPolicy automaticamnte agrega el hostname y nueva key
    #al objeto SSHCLient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print("-----OUTPUT-----")
        for line in output:
            print(line.strip())

def main():
    import getpass
    #getpass puede recuperar el user de la sesion actual
    #oculata el input del password
    #user = input('Username: ')
    #password = getpass.getpass()

    #ip = input('Enter server IP: ')
    #port = input('Enter port: ')
    #cmd = input('Enter command: ')
    command("10.0.2.15", 22,"darkwolf", "Chopipa1", "pwd")

main()

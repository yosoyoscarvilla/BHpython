import paramiko
import shlex
import subprocess

def command(ip, port, user, passwd, cmd):
    client = paramiko.SSHCLient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))
    client.close()
    return

def main():
    import getpass
    #getpass puede recuperar el user de la sesion actual
    #oculata el input del password
    user = input('Username: ')
    password = getpass.getpass()

    ip = input('Enter server IP: ')
    port = input('Enter port: ')
    cmd = input('Enter command: ')
    command(ip, port,user, password, cmd)

main()

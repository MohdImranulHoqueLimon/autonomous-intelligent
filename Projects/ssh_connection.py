import paramiko
import sys

try:
    REDPITAYA_HOST_IP = "192.168.128.1"
    userName = "root"
    password = "root"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    test = ssh.connect(REDPITAYA_HOST_IP, username=userName, password=password)
    # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)

    stdin, stdout, stderr = ssh.exec_command("ls -a")
    lines = stdout.readlines()
    print(lines)

    a = 12313
except:
    print("An exception occurred")
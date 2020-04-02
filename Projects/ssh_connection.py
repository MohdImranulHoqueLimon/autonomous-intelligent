import paramiko
import sys

try:
    REDPITAYA_HOST_IP = "192.168.128.1"
    userName = "root"
    password = "root"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
except:
    print("An exception occurred")
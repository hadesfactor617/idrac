#!/usr/bin/env python3

# import dracclient
# from getpass import getpass
import paramiko
from paramiko import SSHClient, AutoAddPolicy
from paramiko.transport import Transport
# import socket


host = ("192.168.1.98")
port = 22
username = "hadesfactor"
password = "showbiz666!"


client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


try:
    client.connect(host, port=port, username=username, password=password,
                   allow_agent=False, look_for_keys=False)
    transport = client.get_transport()
    transport.auth_interactive_dumb(username, handler=None)
    channel = transport.open_session()
    channel.exec_command("racadm getsysinfo")

    print("idrac version:")
    print(channel.recv(1024).decode('utf-8'))

except paramiko.AuthenticationException:
    print("Authentication failed. Please check your credentials.")
except paramiko.SSHException as e:
    print(f"SSH connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the SSH session
    if client:
        client.close()
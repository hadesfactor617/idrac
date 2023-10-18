#!/usr/bin/env python3

import paramiko
import getpass
import pandas as pd

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# Establish a SSH Connection
def sshConnection(host, port, username, password, rcmd):
    client.connect(host, port, username, password,
                   allow_agent=False, look_for_keys=False)
    transport = client.get_transport()
    transport.auth_interactive_dumb(username, handler=None)
    channel = transport.open_session()

# Exception test
    try:
        channel.exec_command(str(rcmd))
        out = (channel.recv(1024).decode('utf-8'))
        return (out)
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as e:
        print(f"SSH connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Funtion to load Excel, must be .XLS not .XLSX, needs to be in format of
# # "IP" "Host" for Columns with Row1 having the Column Labels
# IP           | Host                    |
# ----------------------------------------
# 192.168.1.1  | something.something.com |
#              |                         |
#              |                         |


def loadIp(filePath):

    IPs = dict()
    try:
        df = pd.read_excel(filePath, skiprows=0)
        for index, row in df.iterrows():
            i = str(row['IP'])
            IPs[i] = str(row['Host'])
    except Exception as e:
        print(e)
    return IPs


def main():

    staticCommand = ('racadm set idrac.webserver.ManualDNSEntry')
    username = input("Please Enter iDrac Username: ")
    password = getpass.getpass(prompt="Please Enter iDrac Password: ")
    port = 22
    IPs = loadIp(input("Enter File Location and Name of XLS containing list of hosts: "))

    for ip, host in IPs.items():
        rcmd = '{} oob-{}'.format(staticCommand, host)
        output = (sshConnection(ip, port, username, password, rcmd))
        print(output)


if __name__ == "__main__":
    main()

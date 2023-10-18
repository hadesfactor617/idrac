#!/usr/bin/env python3

# import dracclient
# from getpass import getpass
import paramiko
# from paramiko import SSHClient, AutoAddPolicy
# from paramiko.transport import Transport
import getpass
import pandas as pd
# import sys
import pprint
import json


client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def runCommand():
    # (input(command+" Type your Rac Command and Press Enter: "))
    # return runCommand
    cmd = input(" Type your Rac Command and Press Enter: ")
    return cmd


# Establish a SSH Connection
def sshConnection(host, port, username, password, rcmd):
    client.connect(host, port, username, password,
                   allow_agent=False, look_for_keys=False)
    transport = client.get_transport()
    transport.auth_interactive_dumb(username, handler=None)
    channel = transport.open_session()

    try:
        # channel.exec_command("racadm getsvctag")
        channel.exec_command(str(rcmd))
        out = (channel.recv(1024).decode('utf-8'))
        return (out)
        # print("Serial:")
        # print(channel.recv(1024).decode('utf-8'))
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as e:
        print(f"SSH connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def loadIp(filePath):

    IPs = dict()
    try:
        df = pd.read_excel(filePath, skiprows=0)
        for index, row in df.iterrows():
            i = str(row['Host'])
            IPs[i] = row
    except Exception as e:
        print(e)
    return IPs


def main():

    username = input("Please Enter iDrac Username: ")
    password = getpass.getpass(prompt="Please Enter iDrac Password: ")
    # username = "hadesfactor"
    # password = "showbiz666!"

    # # uncomment to run the same command across IP list
    # rcmd = runCommand()
    port = 22
    IPs = loadIp(input("Enter File Location and Name of XLS containing list of hosts: "))
    # host = ("192.168.1.98")

    for host in IPs:
        rcmd = runCommand()
        # print('Host: ', host, 'Command: ', rcmd)
        output = (sshConnection(host, port, username, password, rcmd))
        print(output)
        # return (out)
        # test_dict = json.loads(out)
        # print(dict(test_dict))


if __name__ == "__main__":
    main()





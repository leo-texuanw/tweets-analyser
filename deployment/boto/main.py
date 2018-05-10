#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import socket
from mynectar import MyNectar

def get_all_ips(my_nectar):
    ips = []

    reservations = my_nectar.get_all_reservations()
    for idx, _ in enumerate(reservations):
        for instance in reservations[idx].instances:
            ips.append(instance.private_ip_address)
    ips.remove('115.146.95.248')
    print(ips)
    return ips

def write_hosts(server_group, ips):
    hosts = open("../ansible/hosts","w+")

    hosts.write('[' + server_group + ']\n')
    for i in range(0, len(ips)):
        hosts.write(ips[i] + '\n')

    hosts.write('\n[all:vars]\n')
    hosts.write("ansible_ssh_common_args='-o StrictHostKeyChecking=no'\n")
    hosts.write('ansible_ssh_private_key_file=~/.ssh/nectar.key\n')
    hosts.write('ansible_ssh_user=ubuntu\n')

    hosts.close()

def wait_until_running(instance):
    while instance.state != 'running':
        print('WAITING: Instance {} is {}'.format(instance.id, instance.state))
        time.sleep(6)
        instance.update()

    print("SUCCESS: Instance {} is {}".format(instance.id, instance.state))

def until_ssh_port_open(ips):
    SSH_PORT = 22
    for ip in ips:
        result = 1
        while not (result == 0):
            print("Port is not open on ", ip)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip,SSH_PORT))
            time.sleep(5)
        print("Port 22 is open on ", ip)

if __name__ == '__main__':
    """ Execute with: python main.py server_group server_count volume1 volume2 ... """
    server_group = sys.argv[1]
    server_count = sys.argv[2]
    volume_ids = []
    if len(sys.argv) > 3:
        volume_ids = sys.argv[3:]
        print('volume_ids:', volume_ids)

    print('server_count:', server_count)
    my_nectar = MyNectar()

    ## create instances
    instances = my_nectar.launch_instance(server_count)
    print('instances', instances)

    # Instances created successfully
    if instances is not None:
        for i in range(0, int(server_count)):
            instance = instances[i]
            if i < len(volume_ids):
                my_nectar.attach_volume(volume_ids[i], instance)
            else:
                wait_until_running(instance)

        # Write ips to `hosts` file
        ips = get_all_ips(my_nectar)
        write_hosts(server_group, ips)

        until_ssh_port_open(ips)

#!/usr/bin/python
# -*- coding: utf-8 -*-

from mynectar import MyNectar

DB_ANALYSER = 2 # Number of instances for deploying database and analyser
CRAWLER_WEB = 2 # Number of instances for deploying crawler and web server

def get_all_ips(my_nectar):
    ips = []

    reservations = my_nectar.get_all_reservations()
    for idx, _ in enumerate(reservations):
        for instance in reservations[idx].instances:
            ips.append(instance.private_ip_address)
    print(ips)
    return ips

def write_ips_2_hosts(ips):
    hosts = open("../ansible/hosts","w+")

    hosts.write('[db_analyser]\n')
    for i in range(0, DB_ANALYSER):
        hosts.write(ips[i] + '\n')

    hosts.write('\n[crawler_web]\n')
    for i in range(0, CRAWLER_WEB):
        hosts.write(ips[i+DB_ANALYSER] + '\n')

    hosts.close()


if __name__ == '__main__':
    volume_ids = ['vol-431ba098', 'vol-37379a33']

    my_nectar = MyNectar()

    ## create instances
    server_count = DB_ANALYSER + CRAWLER_WEB
    instances = my_nectar.launch_instance(server_count)

    # Instances created successfully
    if instances is not None:
        for i in range(0, DB_ANALYSER):
            instance = instances[i]
            my_nectar.attach_volume(volume_ids[i], instance)

        # Write ips to `hosts` file
        ips = get_all_ips(my_nectar)
        write_ips_2_hosts(ips)


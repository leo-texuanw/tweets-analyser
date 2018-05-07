#!/usr/bin/python
# -*- coding: utf-8 -*-

from mynectar import MyNectar

if __name__ == '__main__':
    my_nectar = MyNectar()
    instances = my_nectar.launch_instance()
    if(instances is not None):
        instance = instances[0]
        volume = my_nectar.create_volume()
        my_nectar.attach_volume(volume, instance)

        reservations = my_nectar.get_all_reservations([instance.id])

        hosts = open("../ansible/hosts","w+")
        hosts.write('[all]\n')


        for idx, res in enumerate(reservations):
            ip = reservations[idx].instances[0].private_ip_address
            print("New instance ip: ", ip)
            hosts.write(ip + '\n')
        hosts.close()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import connect

def list_instances(ec2_conn):

    reservations = ec2_conn.get_all_reservations()

    print('Index\tID\t\tIP\t\tPlacement\tInstance')
    for idx, res in enumerate(reservations):
        print('{}\t{}\t{}\t{}\t{}'.format(idx,
                                    reservations[idx].id,
                                    reservations[idx].instances[0].private_ip_address,
                                    reservations[idx].instances[0].placement,
                                    res.instances))
    return reservations

if __name__ == '__main__':
    ec2_conn = connect.ec2_conn()
    list_instances(ec2_conn)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import connect

def list_volumes(ec2_conn):

    volumes = ec2_conn.get_all_volumes()

    print('Volume ID\t Size(GB)\t Zone\t\t Status\t\t Snapshot ID')
    for vol in volumes:
        print('{}\t {}\t\t {}\t {}\t {}'.format(vol.id, vol.size,
            vol.zone, vol.status, vol.snapshot_id))

    return volumes

if __name__ == '__main__':
    ec2_conn = connect.ec2_conn()
    list_volumes(ec2_conn)

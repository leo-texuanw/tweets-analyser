#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import connect
import constants
from launch_instance import launch

PLACEMENT = constants.PLACEMENT

def demo(ec2_conn):

    instances = launch(ec2_conn, max_instances=1)

    if(instances == None):
        return

    instance = instances[0]
    print('Demo: New instance {} has been created.'.format(instance.id))

    # Request volume
    vol_req = ec2_conn.create_volume(1, PLACEMENT)
    print('Demo: New volume {} has been created.'.format(vol_req.id))

    # Check provisioning status
    curr_vols = ec2_conn.get_all_volumes([vol_req.id])
    print('Volume status: {}, volume AZ: {}: '.format(curr_vols[0].status, curr_vols[0].zone))

    # Check if instance is running
    while (instance.state != 'running'):
        print('Instance {} is {}'.format(instance.id, instance.state))
        time.sleep(5)
        instance.update()

    # Attach volume when instance is ready:
    ec2_conn.attach_volume(vol_req.id, instance.id, '/dev/vdc')
    print('Volume {} has been attached to \{} at /dev/vdc'.format(vol_req.id, instance.id))

    # Create a snapshot
    snapshot = ec2_conn.create_snapshot(vol_req.id, 'Snapshot')
    time.sleep(5)
    print('Snapshot {} has been created.'.format(snapshot.id))

    # Create a volume from the snapshot
    new_vol = snapshot.create_volume(PLACEMENT)
    print('Volume {} has been created by snapshot {}.'.format(new_vol.id, snapshot.id))
    input('Press Enter to continue ...')

    # Delete snapshot
    ec2_conn.delete_snapshot(snapshot.id)
    print('Snapshot {} has been deleted.'.format(snapshot.id))


if __name__ == '__main__':

    ec2_conn = connect.ec2_conn()
    demo(ec2_conn)

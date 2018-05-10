#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from boto import exception as botoException
import connect
import constants as consts

# If `max_instances` can not be fulfilled only one instance will be created
def launch(ec2_conn, max_instances=1):

    try:
        reservation = ec2_conn.run_instances(
            image_id=consts.IMAGE_ID,
            max_count=max_instances,
            key_name=consts.KEY_NAME,
            instance_type=consts.INSTANCE_TYPE,
            security_groups=consts.SECURITY_GROUPS,
            placement=consts.PLACEMENT
        )

        print(reservation)
        print('Reservation.instances:', reservation.instances)

        display_instances(reservation.instances)
    except botoException.EC2ResponseError:
        print(botoException.EC2ResponseError)
        print("FAIL: Create instance failed")
        return None

    return reservation.instances

def display_instances(instances):
    for instance in instances:
        print('SUCC: New instance has been created:')
        print('\tID: {}\tIP: {}\tPlacement: {}\t'.format(instance.id,
                                    instance.private_ip_address,
                                    instance.placement))

if __name__ == '__main__':
    ec2_conn = connect.ec2_conn()
    if len(sys.argv) > 1:
        launch(ec2_conn, int(sys.argv[1]))
    else:
        launch(ec2_conn)

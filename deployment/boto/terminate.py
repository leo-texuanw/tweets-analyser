#!/usr/bin/python
# coding: utf-8

import sys
from boto import exception as botoException
import connect

def terminate(instance_ids):
    ec2_conn = connect.ec2_conn()

    try:
        print('deleting', instance_ids, '...')
        if isinstance(instance_ids, (list,)):
            ec2_conn.terminate_instances(instance_ids=instance_ids)
        else:
            ec2_conn.terminate_instances(instance_ids=[instance_ids])
        print('Now instance {} has been terminated.'.format(instance_ids))

    except botoException.EC2ResponseError:
        print('EC2ResponseError: ', botoException.EC2ResponseError)
        print('Invalid instance_id(s) or try again later')
        return False

    return True

if __name__ == '__main__':
    instance_ids = sys.argv[1:]
    terminate(instance_ids)

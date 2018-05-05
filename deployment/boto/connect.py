#!/usr/bin/python
# coding: utf-8

import boto
from boto.ec2.regioninfo import RegionInfo
import constants as consts

def ec2_conn():
    region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

    ec2_conn = boto.connect_ec2(aws_access_key_id=consts.ACCESS_KEY_ID,
                            aws_secret_access_key=consts.SECRET_ACCESS_KEY,
                            is_secure=True,
                            region=region,
                            port=8773,
                            path='/services/Cloud',
                            validate_certs=False)
    return ec2_conn

if __name__ == '__main__':
    ec2_conn()

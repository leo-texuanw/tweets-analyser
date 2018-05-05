#!/usr/bin/python
# coding: utf-8

import connect
import terminate

ec2_conn = connect.ec2_conn()
all = ec2_conn.get_all_instances()
for i in all:
    print(i.id)
terminate.terminate(['i-503870a0'])

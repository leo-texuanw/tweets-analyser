#!/usr/bin/python
# coding: utf-8

import connect

def list_images():
    ec2_conn = connect.ec2_conn()

    images = ec2_conn.get_all_images()
    for img in images:
        print('Image id: {}, Image name: {}'.format(img.id, img.name))

if __name__ == '__main__':
    list_images()

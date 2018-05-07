# -*- coding: utf-8 -*-

import time
import boto
from boto.ec2.regioninfo import RegionInfo
from boto import exception as botoException

class MyNectar:
    """ This is a class containing Nectar operation functions.  """

    def __init__(self):
        self.access_key_id = 'c6ba6f8fbbbe4e56879fd23610617247'
        self.secret_access_key = 'fe369349b39c4d13b107209d5ab22dca'

        self.image_id = 'ami-b481405b'
        self.key_name = 'nectar'
        self.placement = 'melbourne-np'
        self.instance_type = 'm1.medium'
        self.security_groups = ['default', 'couchDB']

        self.ec2_conn = self.__connect__()

    def __connect__(self):
        """ Connect to Nectar"""

        region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

        ec2_conn = boto.connect_ec2(aws_access_key_id=self.access_key_id, \
                aws_secret_access_key=self.secret_access_key, \
                is_secure=True, \
                region=region, \
                port=8773, \
                path='/services/Cloud', \
                validate_certs=False)
        return ec2_conn

    # Instances Operation
    def launch_instance(self, max_instances=1):
        """ To launch a new instance. If `max_instances` cannot be fulfilled,
            only minimum instance, default as 1, will be established.
        """
        try:
            reservation = self.ec2_conn.run_instances(
                image_id=self.image_id,
                max_count=max_instances,
                key_name=self.key_name,
                instance_type=self.instance_type,
                security_groups=self.security_groups,
                placement=self.placement
            )

            print(reservation)
            print('Reservation.instances:', reservation.instances)

            MyNectar.display_instances(reservation.instances)
        except botoException.EC2ResponseError:
            print(botoException.EC2ResponseError)
            print("FAIL: Create instance failed")
            return None

        return reservation.instances

    @staticmethod
    def display_instances(instances):
        """ Formatly display instances """
        for instance in instances:
            print('SUCC: New instance has been created:')
            print('\tID: {}\tIP: {}\tPlacement: {}\t'.format( \
                    instance.id, instance.private_ip_address, instance.placement))


    def get_all_reservations(this, instance_ids=None):
        """ Fetch all reservations """
        reservations = this.ec2_conn.get_all_reservations(instance_ids)

        print('Index\tID\t\tIP\t\tPlacement\tInstance')
        for idx, res in enumerate(reservations):
            print('{}\t{}\t{}\t{}\t{}'.format( \
                idx, reservations[idx].id, \
                reservations[idx].instances[0].private_ip_address, \
                reservations[idx].instances[0].placement, \
                res.instances))
        return reservations

    # Volumes Operation
    def create_volume(self, size=50):
        """ Create volumes """
        volume = self.ec2_conn.create_volume(size, self.placement)
        print('New volume {} has been created.'.format(volume.id))
        return volume

    def get_volumes(self, volume_ids=None):
        """ Get volumes associated with `volumes_ids`.
            Get all volumes if `volume_ids` is not provided.
        """
        curr_vols = self.ec2_conn.get_all_volumes(volume_ids)
        print('Volume status: {}, volume AZ: {}: '.format(curr_vols[0].status, curr_vols[0].zone))
        return curr_vols


    def attach_volume(self, volume, instance):
        """ Attach volume when instance is ready """

        print("volume status:", volume.status)

        # check if instance status is "running"
        while instance.state != 'running':
            print('WAITING: Instance {} is {}'.format(instance.id, instance.state))
            time.sleep(6)
            instance.update()

        print("SUCCESS: Instance {} is {}".format(instance.id, instance.state))

        self.ec2_conn.attach_volume(volume.id, instance.id, '/dev/vdc')
        print('Volume {} has been attached to \{} at /dev/vdc'.format(volume.id, instance.id))

from connect import ec2_conn
import constant

reservation = ec2_conn.run_instances('ami-b481405b',
                                     key_name='nectar',
                                     instance_type=constant.INSTANCE_TYPE,
                                     security_groups=['default'],
                                     placement=constant.PLACEMENT)

instance = reservation.instances[0]
print('New instance {} has been created.'.format(instance.id))

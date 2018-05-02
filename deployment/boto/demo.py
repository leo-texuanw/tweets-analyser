import time
import constant
from connect import ec2_conn

PLACEMENT = constant.PLACEMENT
reservation = ec2_conn.run_instances('ami-b481405b',
                                     key_name='nectar',
                                     #instance_type='m1.medium',
                                     instance_type='m2.small',
                                     security_groups=['default'],
                                     placement=PLACEMENT)

instance = reservation.instances[0]
print('New instance {} has been created.'.format(instance.id))

# Request volume
vol_req = ec2_conn.create_volume(1, PLACEMENT)
print('New volume {} has been created.'.format(vol_req.id))

# Check provisioning status
curr_vols = ec2_conn.get_all_volumes([vol_req.id])
print('Volume status: {}, volume {}: '.format(curr_vols[0].status, curr_vols[0].id))

# Check if instance is running
while (instance.state != 'running'):
    print('Instance {} is {}'.format(instance.id, instance.state))
    time.sleep(5)
    instance.update()

# Attach volume when instance is ready:
ec2_conn.attach_volume(vol_req.id, instance.id, '/dev/vdc')
print('Volume {} has been attached to \{} at /dev/vdc'.format(vol_req.id))

# Create a snapshot
snapshot = ec2_conn.create_snapshot(vol_req.id, 'Snapshot')
time.sleep(5)
print('Snapshot {} has been created.'.format(snapshot.id))

# Create a volume from the snapshot
new_vol = snapshot.create_volume(PLACEMENT)
print('Volume {} has been created snapshot {}.'.format(new_vol.id))
input('Press Enter to continue ...')

# Delete snapshot
ec2_conn.delete_snapshot(snapshot.id)
print('Snapshot {} has been deleted.'.format(snapshot.id))

from connect import ec2_conn

def terminate(instance_id):
    if isinstance(instance_id, (list,)):
        ec2_conn.terminate_instances(instance_ids=instance_id)
    else:
        ec2_conn.terminate_instances(instance_ids=[instance_id])
    print('Now instance {} has been terminated.'.format(instance_id))

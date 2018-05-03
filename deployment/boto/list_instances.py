from connect import ec2_conn

reservations = ec2_conn.get_all_reservations()

print('Index\tID\t\tIP\t\tInstance\tPlacement')
for idx, res in enumerate(reservations):
    print('{}\t{}\t{}\t{}\t{}'.format(idx,
                                reservations[idx].id,
                                reservations[idx].instances[0].private_ip_address,
                                reservations[idx].instances[0].placement,
                                res.instances))


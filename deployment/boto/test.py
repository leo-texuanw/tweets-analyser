from connect import ec2_conn
import terminate

all = ec2_conn.get_all_instances()
for i in all:
    print(i.id)
terminate.terminate(['i-503870a0'])

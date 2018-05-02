import boto
import constant
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

ec2_conn = boto.connect_ec2(aws_access_key_id=constant.ACCESS_KEY_ID,
                            aws_secret_access_key=constant.SECRET_ACCESS_KEY,
                            is_secure=True,
                            region=region,
                            port=8773,
                            path='/services/Cloud',
                            validate_certs=False)

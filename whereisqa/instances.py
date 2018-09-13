from dataclasses import dataclass

import boto3

import config

from pprint import pprint


@dataclass
class Environment:
    name: str = ''
    webserver_ip: str = ''
    worker_ip: str = ''
    scheduler_ip: str = ''


ENVIRONMENTS = {
    'qa': Environment(),
    'ux': Environment(),
    'ppe': Environment(),
    'prod': Environment(),
}


def create_inventory():
    pass


def get_tag_value(key, tags, *, strict=True):
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']

    if strict:
        raise ValueError('No such key %s' % key)


def update_record(env, instance_type, ip_address):
    pass


def show():
    ec2 = boto3.client(
        'ec2',
        region_name='us-east-1',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    )
    filters = [
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    # filter the instances based on filters() above
    # instances = ec2.instances.filter(Filters=filters)
    # for i in ec2.describe_instances():
    #     import pdb; pdb.set_trace()
    #     print(i)
    response = ec2.describe_instances(
        Filters=filters
    )
    reservations = response['Reservations']
    instances = [r['Instances'][0] for r in reservations]
    for i in instances:
        tags = i.get('Tags')
        ip = i.get('PublicIpAddress')
        if ip is None or tags is None:
            continue

        env = get_tag_value('env', tags, strict=False)
        instance_type = get_tag_value('type', tags, strict=False)
        if env is None or instance_type is None:
            continue
        
        update_record(env, instance_type, ip)

show()

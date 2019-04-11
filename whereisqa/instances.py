from typing import List
from dataclasses import dataclass, field

import boto3

import config
from whereisqa.utils import logger


@dataclass
class Environment:
    name: str = ''
    webservers: List[str] = field(default_factory=lambda: [])
    workers: List[str] = field(default_factory=lambda: [])
    schedulers: List[str] = field(default_factory=lambda: [])


def create_inventory():
    inventory = {
        'qa': Environment(name='qa'),
        'ux': Environment(name='ux'),
        'ppe': Environment(name='ppe'),
        'prod': Environment(name='prod'),
    }
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
    response = ec2.describe_instances(Filters=filters)
    reservations = response['Reservations']
    instances = [r['Instances'][0] for r in reservations]
    for i in instances:
        instance_id = i['InstanceId']
        tags = i.get('Tags')
        ip = i.get('PublicIpAddress')
        if ip is None or tags is None:
            logger.debug('Ignoring %s instance', instance_id)
            continue

        env_name = get_tag_value('env', tags, strict=False)
        instance_type = get_tag_value('type', tags, strict=False)
        if env_name is None or instance_type is None:
            logger.debug('%s is not our target instance, '
                         'missing required tags', instance_id)
            continue

        update_record(inventory, env_name, instance_type, ip)

    return inventory


def get_tag_value(key, tags, *, strict=True):
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value']

    if strict:
        raise ValueError('No such key %s' % key)


# todo (misha): this one is not pure function. Consider refactoring
def update_record(inventory, env_name, instance_type, ip_address):
    def get_env_key():
        mapping = {
            'qa': 'qa',
            'ux': 'ux',
            'test': 'ppe',
            'prod': 'prod',
        }
        return mapping.get(env_name)

    env_key = get_env_key()
    if env_key is None:
        logger.debug('env %s ignored', env_key)
        return

    env = inventory[env_key]
    prop = f'{instance_type}s'
    getattr(env, prop).append(ip_address)

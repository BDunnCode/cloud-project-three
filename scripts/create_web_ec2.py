#!/usr/bin/env python3

import boto3

# Replace these with real, working values from your setup
AMI_ID = 'ami-0ddac208607ae06a0'  # Another more recent AMI may be preferable.
INSTANCE_TYPE = 't2.micro'
KEY_NAME = 'my-key-pair'
SECURITY_GROUP_IDS = ['sg-abcdefgh1234567']
SUBNET_ID = 'subnet-abcdefgh1234567'

def launch_instance():
    ec2 = boto3.client('ec2')

    response = ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=SECURITY_GROUP_IDS,
        SubnetId=SUBNET_ID,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'Python-Launched-Instance'}]
            }
        ]
    )

    instance_id = response['Instances'][0]['InstanceId']
    print(f"Launched instance with ID: {instance_id}")

if __name__ == "__main__":
    launch_instance()
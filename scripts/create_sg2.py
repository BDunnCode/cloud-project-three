import boto3

# CONFIGURE THIS SECTION
SECURITY_GROUP_NAME = "cp3-db-sg"
DESCRIPTION = "Security group for db tier (MySQL + SSH)"
VPC_ID = "vpc-abcdefgh1234567"  # Replace with your actual VPC ID
REGION = "us-east-2"
WEB_SECURITY_GROUP_ID = "sg-abcdefgh1234567"  # Replace with actual Web SG ID

# Initialize EC2 client
ec2 = boto3.client('ec2', region_name=REGION)

# Create the security group
response = ec2.create_security_group(
    GroupName=SECURITY_GROUP_NAME,
    Description=DESCRIPTION,
    VpcId=VPC_ID,
    TagSpecifications=[
        {
            'ResourceType': 'security-group',
            'Tags': [
                {'Key': 'Name', 'Value': SECURITY_GROUP_NAME},
                {'Key': 'Project', 'Value': '2-tier-app'}
            ]
        }
    ]
)

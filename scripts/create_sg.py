import boto3

# CONFIGURE THIS SECTION
SECURITY_GROUP_NAME = "cp3-web-sg"
DESCRIPTION = "Security group for web tier (HTTP + SSH)"
VPC_ID = "vpc-e78c449f72375e007"  # <-- Replace with your actual VPC ID
REGION = "us-east-1"

# Initialize EC2 client
ec2 = boto3.client('ec2', endpoint_url='http://localhost:4566')

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

security_group_id = response['GroupId']
print(f"Created security group with ID: {security_group_id}")

# Add inbound rules (HTTP and SSH)
ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'Allow HTTP'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'Allow SSH'}]
        }
    ]
)

print("Inbound rules added.")
# 📦 Project Overview

Fix this w/ copy paste from version on home pc

# 🛠️ Tools Used / Tech Stack

| Layer         | Tech Stack       | Purpose                                      |
|---------------|------------------|----------------------------------------------|
| Web Server    | Python + Flask   | Handles form input and HTML output           |
| Frontend      | HTML + CSS       | Builds the UI: input, button, output table   |
| Backend       | Flask (Python)   | Logic + DB interactions                      |
| Database      | MySQL on EC2     | Stores guestbook entries                     |
| Infrastructure| AWS EC2 (2x)     | Web + DB tiers                               |
| Deployment    | Manual (SSH)     | SSH + install packages via CLI               |
| Security      | Security Groups  | HTTP/SSH for web, 3306 from web-only         |

# 📜 Network Diagrams

# ✍️ Design Rationale and 💰 Cost Savings

maybe fix this with home version on PC

# 🔧 Build Process

## Prerequisites

This project assumes that you've already completed "cloud-project-two" linked in the "Project Overview" section.

For the sake of conserving resources, you'll be reusing the VPC and subnets from that project. Before starting the 
"Create Security Groups" section be certain that you have:

- A VPC
- A public subnet
- A private subnet
- Internet Gateway
- Route Table?

// The internet gateway has to be attached to something, rather the something has to have an internet 
gateway attached, I believe. I'm pretty sure this gets attached to the VPC to allow internet traffic 
to happen. I need to clarify this.

## Create Security Groups

In your WSL Ubuntu bash shell, type:

```bash
nano create_sg.py
```

paste in the following:

```bash
import boto3

# CONFIGURE THIS SECTION
SECURITY_GROUP_NAME = "web-sg"
DESCRIPTION = "Security group for web tier (HTTP + SSH)"
VPC_ID = "vpc-040fca4e38b58d593"  # <-- Replace with your actual VPC ID
REGION = "us-east-1" #<--- Replace with your actual region

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
```

Once that script is entered into the file and you've filled in your information, save and exit nano, then run the script using:

```bash
python3 create_sg.py
```


We'll now create the other security group for the database tier. This is mostly just a few modifications on the script used for the 
web security group. 

Open a new nano file:

```bash
nano create_sg2.py
```

Paste in the following:

```bash
import boto3

# CONFIGURE THIS SECTION
SECURITY_GROUP_NAME = "cp3-db-sg"
DESCRIPTION = "Security group for db tier (MySQL + SSH)"
VPC_ID = "vpc-040fca4e38b58d593"  # Replace with your actual VPC ID
REGION = "us-east-2"
WEB_SECURITY_GROUP_ID = "sg-xxxxxxxxxxxxxxxxx"  # Replace with actual Web SG ID

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

security_group_id = response['GroupId']
print(f"Created security group with ID: {security_group_id}")

# Add inbound rules
ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 3306,
            'ToPort': 3306,
            'UserIdGroupPairs': [
                {
                    'GroupId': WEB_SECURITY_GROUP_ID,
                    'Description': 'Allow MySQL from web SG'
                }
            ]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [
                {'CidrIp': '207.223.37.25/32', 'Description': 'Allow SSH'}
            ]
        }
    ]
)

print("Inbound rules added.")
```

## Create the EC2 instances

Now that we've created our security groups, let's generate the instances for our web delivery and database.

### Creating the Web Server

In the follow scripts you'll have to fill in your own security group, subnet, and key pair information. 
There will be an AMI id included, but if you're looking for a newer one, you can use the get_ami.py script
found in the scripts folder in the github repository.

Now, type

```bash
nano create_web_ec2.py
```

and paste in the following script:

```bash
#!/usr/bin/env python3

import boto3

# Replace these with real, working values from your setup
AMI_ID = 'ami-0ddac208607ae06a0'  # Amazon Linux 2
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
```
You can adjust the name in the AWS console, or id the tagspecifications section in the script if you'd like.
My instance is called cp3-guestbook-web. Now, we'll move towards creating the database server.

### Creating the Database Server

Creating the database server is effectively identical to creating the web server, except for the security group and subnets that will be attached. We want the web server on a public subnet

# 🤔 Reflections



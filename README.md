# 📦 Project Overview

Fix this w/ copy paste from version on home pc

# 🛠️ Tools Used / Tech Stack

Web Server | Python + Flask	| Handles form + output
Frontend |	HTML + CSS |	Input field, submit button, table
Backend	| Python	Flask | handles DB + rendering
Database | 	MySQL on EC2 |	Stores guestbook entries
Infra	| AWS EC2 (2x)	| Web + DB tiers, SSH into both
Deployment |	Manual setup	| SSH + sudo apt install for setup
Security |	Security groups |	Only allow web-to-DB traffic on port 3306

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

Now that we've got the appropriate security groups made



# 🤔 Reflections



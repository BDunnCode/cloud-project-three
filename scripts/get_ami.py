import boto3

def get_amazon_linux_2_ami():
        ec2 = boto3.client('ec2')

        response = ec2.describe_images(
        Owners=['amazon'],
        Filters=[
                {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
                {'Name': 'state', 'Values': ['available']},
                {'Name': 'architecture', 'Values': ['x86_64']},
                {'Name': 'root-device-type', 'Values': ['ebs']},
                {'Name': 'virtualization-type', 'Values': ['hvm']}
        ]
        )

        # Sort by CreationDate descending to get the latest one
        images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
        latest_ami = images[0]
        print(f"Latest Amazon Linux 2 AMI ID: {latest_ami['ImageId']}")
        print(f"Name: {latest_ami['Name']}")
        print(f"Creation Date: {latest_ami['CreationDate']}")

if __name__ == "__main__":
        get_amazon_linux_2_ami()


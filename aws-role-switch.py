# This code demonstrates how to 
# switch role through python boto

import  boto3, argparse, sys

# Collect aws access key, secrect key, target role arn passed as command line parameters
# iam user who runs this script need to provide its own aws access key and secret key
# target role can exist within the iam user's own aws account or can be cross account

parser = argparse.ArgumentParser(description='Usage:')
parser.add_argument('-a', '--access_key', action='store', dest='access_key', required=True, help='AWS access key')
parser.add_argument('-s', '--secret_key', action='store', dest='secret_key', required=True, help='AWS secret key')
parser.add_argument('-r', '--role_arn', action='store', dest='role_arn', required=True, help='AWS role arn')

args = parser.parse_args()

if len(sys.argv) == 1 or (args.access_key).isspace() or (args.secret_key).isspace() or (args.role_arn).isspace():
    parser.print_help()
    parser.exit(1)

# Create sts object to assume target role 
sts_client = boto3.client('sts', aws_access_key_id=args.access_key, aws_secret_access_key=args.secret_key)

# Assume the target role
role_obj = sts_client.assume_role( RoleArn=args.role_arn, RoleSessionName='mysession')

# Get temporary credentials 
credentials_temp = role_obj['Credentials']

# Get temp access key, secret key, session token from target role
aws_access_key = credentials_temp['AccessKeyId']
aws_secret_key = credentials_temp['SecretAccessKey']
aws_session_token = credentials_temp['SessionToken']


# Example, use the temporary role to describe regions
ec2_client = boto3.client('ec2',
                   aws_access_key_id=aws_access_key,
                   aws_secret_access_key=aws_secret_key,
                   aws_session_token =aws_session_token) 
print(ec2_client.describe_regions())

## Example run
## python aws-role-switch.py -a AKIXXX -s KxYYY -r arn:aws:iam::ZZZ

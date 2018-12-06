AWSTemplateFormatVersion: 2010-09-09
Description: "Create ssh keypair"

Parameters:
  ModuleName:
    Description: The name of the python file
    Type: String
    Default: index.handler
  RandomValue:
    Description: Assign an unique value on stack update
    Type: String
Resources:

    LambdaExecutionRole:
      Type: 'AWS::IAM::Role'
      Properties:
        AssumeRolePolicyDocument:
          Version: 2012-10-17
          Statement:
            - Effect: Allow
              Principal:
                Service:
                  - lambda.amazonaws.com
              Action:
                - 'sts:AssumeRole'
        Path: /
        Policies:
          - PolicyName: root
            PolicyDocument:
              Version: 2012-10-17
              Statement:
                - Effect: Allow
                  Action:
                    - 'logs:CreateLogGroup'
                    - 'logs:CreateLogStream'
                    - 'logs:PutLogEvents'
                  Resource: 'arn:aws:logs:*:*:*'
                - Effect: Allow
                  Action:
                   - 'ec2:CreateKeyPair'
                   - 'ec2:DescribekeyPairs'
                   - 'ssm:GetParameters'
                   - 'ssm:PutParameter'
                  Resource: '*'

    SSHKeyPairFunction:
      Type: AWS::Lambda::Function
      Properties:
        Description: Creates ssh keypair 
        Code:
          ZipFile: |
            import boto3
            import cfnresponse
            def handler(event, context):
              try:
                responseValue = event['RequestType']
                responseData = {}
                responseData['Data'] = responseValue + ' successful!'
                print(responseValue)
                ec2_client = boto3.client('ec2')
                ssm_client = boto3.client('ssm')
                tag = ssm_client.get_parameters(Names=['mastertag',], WithDecryption=True)
                keypair_name = tag['Parameters'][0]['Value'] + '-keypair'  
                response = ec2_client.describe_key_pairs(KeyNames=[keypair_name]) 
                print('Found! keypair already exist.')
                cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)
              except Exception as err:
                if err.response["Error"]["Code"] == "InvalidKeyPair.NotFound":
                  print('Not Found! Generating a new key pair.')
                  keypair = ec2_client.create_key_pair(KeyName=keypair_name)
                  response = ssm_client.put_parameter(Name=keypair_name, Value=keypair['KeyMaterial'],Type='String')
                  cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)   
              finally:
                print('Finally getting executed!')
                cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)

        Handler: !Ref ModuleName # must be index.handler if inline code provided
        Role: !GetAtt LambdaExecutionRole.Arn
        Runtime: python3.6
        Timeout: '30'

    SSHKeyPair:
      Type: Custom::SSHKeyPair
      Properties:
        ServiceToken: !GetAtt SSHKeyPairFunction.Arn
        Region: !Ref AWS::Region 
        CustomeRandomValue: !Ref RandomValue

      # TIP:
      # Any lambda function code changes (inline or s3 file) of the custome resource has no effect when you update the stack
      # thinking CF will deploy and run the changed lambda code. CF deploys and run the custom lambda only the first time and
      # subsequent lambda code changes are ignored by CF. The workaround is to have a 'RandomValue' paramater, declaring a 
      # property in custom resourace and pass unique random value during stack update.
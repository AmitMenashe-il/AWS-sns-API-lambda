import boto3
import json
from botocore.errorfactory import ClientError

LAMBDA_IAM_ROLE_NAME = "LambdaBasicExecution"
LAMBDA_LOGS_POLICY_NAME = 'LambdaLogsDefaultPolicy'
LAMBDA_PUBLISHSNS_POLICY_NAME = 'PublishSnsLambdaPolicy'


def create_lambda_logs_policy(lambda_name: str) -> str:
    print('trying to Create lambda logs policy - LambdaLogsDefaultPolicy..')
    iam = boto3.client('iam')
    with open('lambda_logs_policy.json') as f:
        policy = json.load(f)
    # replace placeholder with lambda_name
    policy['Statement'][1]['Resource'][0] = policy['Statement'][1]['Resource'][0].replace('{{lambda_name}}',
                                                                                          lambda_name)
    lambda_logs_policy_resource = iam.create_policy(PolicyName=LAMBDA_LOGS_POLICY_NAME,
                                                    PolicyDocument=json.dumps(policy))
    print('Creating lambda logs policy - LambdaLogsDefaultPolicy - Complete')
    return lambda_logs_policy_resource['Policy']['Arn']


def create_lambda_publishSNS_policy(topic_arn: str) -> str:
    print('trying to Create lambda publishSNS policy - LambdaLogsDefaultPolicy...')
    iam = boto3.client('iam')
    with open('lambda_publishSNS_policy.json') as f:
        policy = json.load(f)
    # replace placeholder with topic_arn
    policy['Statement'][0]['Resource'] = topic_arn
    publishSNS_policy_resource = iam.create_policy(PolicyName=LAMBDA_PUBLISHSNS_POLICY_NAME,
                                                   PolicyDocument=json.dumps(policy))
    print('Creating lambda publishSNS policy - LambdaLogsDefaultPolicy - Complete')
    return publishSNS_policy_resource['Policy']['Arn']


def create_lambda_role(lambda_role_name: str):
    print(f'trying to Create lambda LambdaBasicExecution Role - {lambda_role_name}...')
    iam = boto3.client('iam')
    with open('lambda_role.json') as f:
        role_json = f.read()
    iam.create_role(
        RoleName=lambda_role_name,
        AssumeRolePolicyDocument=role_json
    )
    print(f'Creating lambda LambdaBasicExecution Role - {lambda_role_name} - Complete')


def create_lambda_role_and_assign_policy(lambda_name: str, topic_arn: str) -> str:
    # creates lambda role ans assigns logs policy, sns publish policy into role

    iam = boto3.client('iam')

    # using try/except and booleans instead of checking if roles exists for wider exception handling
    lambdaRoleCreated = False
    logsPolicyCreated = False
    publishSNSPolicyCreated = False

    # call role functions:
    try:

        create_lambda_role(LAMBDA_IAM_ROLE_NAME)
        lambdaRoleCreated = True
        print(f'lambda role created, {E}')
    except ClientError as E:
        print(f'\tlambda role not created, {E}')

    try:
        lambda_logs_policy_arn = create_lambda_logs_policy(lambda_name)
        logsPolicyCreated = True
        print(f'lambda logs policy created')
    except ClientError as E:
        print(f'\tlambda logs policy not created, {E}')

    try:
        lambda_publishSNS_policy_arn = create_lambda_publishSNS_policy(topic_arn)
        publishSNSPolicyCreated = True
        print(f'lambda publishSNS policy created')
    except ClientError as E:
        print(f'\tpublishSNS policy not created, {E}')

    iamRole = boto3.resource('iam')
    if lambdaRoleCreated or logsPolicyCreated or publishSNSPolicyCreated:
        lambda_role_resource = iamRole.Role(LAMBDA_IAM_ROLE_NAME)

    # attach policies to role:
    if lambdaRoleCreated:
        lambda_role_resource.attach_policy(PolicyArn=lambda_logs_policy_arn)
        lambda_role_resource.attach_policy(PolicyArn=lambda_publishSNS_policy_arn)
    elif publishSNSPolicyCreated:
        lambda_role_resource.attach_policy(PolicyArn=lambda_publishSNS_policy_arn)
    elif logsPolicyCreated:
        lambda_role_resource.attach_policy(PolicyArn=lambda_logs_policy_arn)

    lambda_iam_role_arn = iam.get_role(RoleName=LAMBDA_IAM_ROLE_NAME)
    return lambda_iam_role_arn['Role']['Arn']

import boto3
import os


def create_lambda(lambda_name: str, lambda_role: str, lambda_code_zip_file: str) -> str:
    client = boto3.client('lambda')
    lambda_filename = os.path.splitext(lambda_code_zip_file)[0]
    if not os.path.exists(lambda_code_zip_file):
        try:
            create_zip_from_py(lambda_filename + '.py')
        except Exception as e:
            raise 'cannot find lambda code file!'
    with open(lambda_code_zip_file, 'rb') as f:
        lambda_code = f.read()

    lambda_runtime = 'python3.9'
    handler = f'{lambda_filename}.lambda_handler'
    code = dict(ZipFile=lambda_code)

    try:
        response = client.create_function(FunctionName=lambda_name, Runtime=lambda_runtime, Role=lambda_role, Code=code,
                                          Handler=handler)
        print('lambda function created')
        return response['FunctionArn']
    except client.exceptions as E:
        print(f'\terror creating lambda function {E}')


def get_lambda_function_arn_by_name(function_name: str) -> str:
    client = boto3.client('lambda')
    response = client.list_functions()

    for function in response['Functions']:
        if function['FunctionName'] == function_name:
            return function['FunctionArn']
    return None


def check_lambda_exists(function_name: str) -> bool:
    if get_lambda_function_arn_by_name(function_name):
        return True
    return False


def delete_lambda_function(lambda_function_name: str):
    client = boto3.client('lambda')

    try:
        # delete function returns response but data not useful
        client.delete_function(FunctionName=lambda_function_name)
        print(f'Deleted existing lambda function {lambda_function_name}')
    except client.exceptions.ResourceNotFoundException as E:
        print(f"\tLambda function '{lambda_function_name}' not deleted, {E}")


def create_api_trigger(lambda_name: str, api_id: str):
    client = boto3.client('lambda')
    try:
        client.add_permission(
            FunctionName=lambda_name,
            StatementId='AllowInvokeFromApiGateway',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-1:264782567005:{api_id}/*/POST/{lambda_name}'
        )
        print(f'created trigger for {lambda_name} by api')
    except ClientError as E:
        print(f'\terror creating api gateway trigger to lambda {E}')


def create_sns_trigger(lambda_name: str, topic_arn: str):
    client = boto3.client('lambda')
    try:
        client.add_permission(
            FunctionName=lambda_name,
            StatementId='sns-trigger',
            Action='lambda:InvokeFunction',
            Principal='sns.amazonaws.com',
            SourceArn=topic_arn
        )
        topic_name = topic_arn.split(':')[-1]
        print(f'created trigger for {lambda_name} for topic {topic_name}')
    except ClientError as E:
        print(f'\tLambda trigger to topic {topic_arn} not created, {E}')
import boto3
from zipfile import ZipFile
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


def update_lambda_code_file(file_name: str, new_topic_arn: str):
    updated_lines = []

    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith('    topic_arn = '):
                updated_lines.append(f"    topic_arn = '{new_topic_arn}'\n")
            else:
                updated_lines.append(line)

        with open(file_name, 'w') as file:
            file.writelines(updated_lines)

        print(f'lambda code file {file_name} updated with new topic ARN')
    except Exception as E:
        print(f'\tcant update lambda code file {file_name}! {E}')


def create_zip_from_py(file_name: str):
    zip_file_name = file_name.replace('.py', '.zip')
    try:
        with ZipFile(zip_file_name, 'w') as z:
            z.write(file_name)
    except Exception as E:
        print(f'\tCant create lambda zip file {zip_file_name} from {file_name}, {E}')
    print('lambda zip file created')

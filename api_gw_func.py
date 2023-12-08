import boto3
from botocore.exceptions import ClientError


def create_api_gateway(api_name: str, lambda_name: str, lambda_arn: str) -> str:
    try:
        apiGW = boto3.client('apigatewayv2')
        res = apiGW.create_api(
            ProtocolType="HTTP",
            Name=api_name,
            RouteKey="POST /" + lambda_name,
            Target=lambda_arn
        )
        print('api gateway created')
        return res['ApiId']
    except ClientError as E:
        print(f'\t api gateway no created {E}')


def create_api_trigger(lambda_name: str, api_id: str):
    lambdaC = boto3.client('lambda')
    try:
        lambdaC.add_permission(
            FunctionName=lambda_name,
            StatementId='AllowInvokeFromApiGateway',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-1:264782567005:{api_id}/*/POST/{lambda_name}'
        )
        print(f'created trigger for {lambda_name} by api')
    except ClientError as E:
        print(f'\terror creating api gateway trigger to lambda {E}')


def get_api_gateway_id_by_name(api_name: str) -> str:
    apiGateway_client = boto3.client('apigatewayv2')

    apis = apiGateway_client.get_apis()

    for api in apis['Items']:
        if api['Name'] == api_name:
            return api['ApiId']
    return None


def check_api_gateway_id_by_name(api_name: str) -> bool:
    if get_api_gateway_id_by_name(api_name):
        return True
    return False

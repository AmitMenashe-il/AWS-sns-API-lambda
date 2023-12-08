import boto3
from botocore.exceptions import ClientError


def format_sns_message_attribute(data_type: str, value: str) -> dict:
    # IMPORTANT REMINDER -  when sending datatype 'Number', item recieved as type 'String', when sending 'StringValue' recieved as 'Value'
    try:
        numeric_value = float(value)
        return {
            "DataType": data_type,
            "StringValue": str(numeric_value)
        }
    except ValueError:
        return {
            "DataType": data_type,
            "StringValue": "0"
        }


def create_sns_topic(name: str) -> str:
    sns = boto3.client('sns')
    try:
        topic = sns.create_topic(Name=name)
        print(f'topic: {name}, created')
    except ClientError as E:
        print(f'\ttopic: {name}, not created, {E}')
    return topic['TopicArn']


def create_sns_subscription(topic_arn: str, protocol: str, subscriber: str):
    sns = boto3.client('sns')
    sns.subscribe(TopicArn=topic_arn, Protocol=protocol, Endpoint=subscriber)
    topic_name = topic_arn.split(':')[-1]
    print(f'{protocol} subscription created for {subscriber} to topic {topic_name}')


def check_sns_protocol_subscribed(topic_arn: str, protocol: str, email: str) -> bool:
    sns_client = boto3.client('sns')
    response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)

    for subscription in response['Subscriptions']:
        if subscription['Protocol'] == protocol and subscription['Endpoint'] == email:
            return True
    return False


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


def get_topic_arn_by_name(topic_name: str) -> str:
    sns_client = boto3.client('sns')
    response = sns_client.list_topics()
    if 'Topics' in response:
        for topic in response['Topics']:
            if topic_name in topic['TopicArn']:
                return topic['TopicArn']
    return None


def check_sns_topic_existence(topic_name: str) -> bool:
    if get_topic_arn_by_name(topic_name):
        return True  # Topic exists
    return False


def send_sns_message(topic_arn: str, num1: str, num2: str) -> str:
    # uses a format function to send the numbers in the SNS message, please note reminder in format function

    sns = boto3.client('sns')
    message = f"Message sent by SNS - numbers: {num1} and {num2}"
    messageAttributes = {
        "Num1": format_sns_message_attribute("Number", num1),
        "Num2": format_sns_message_attribute("Number", num2)
    }
    sns.publish(TopicArn=topic_arn, Message=message, MessageAttributes=messageAttributes)
    return message

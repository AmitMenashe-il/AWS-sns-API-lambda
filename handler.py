import boto3


def lambda_handler(event: dict, context: dict) -> dict:
    sns = boto3.client('sns')
    # note the topic_arn line is being addressed in aws_lambda_functions.py update_lambda_code_file function
    topic_arn = 'arn:aws:sns:us-east-1:264782567005:SNS_Send'

    # request from sns
    if 'Records' in event and 'Sns' in event['Records'][0]:
        num1 = event['Records'][0]['Sns']['MessageAttributes']['Num1']['Value']
        num2 = event['Records'][0]['Sns']['MessageAttributes']['Num2']['Value']
        snsMessage: str = event['Records'][0]['Sns']['Message']
    else:
        snsMessage: bool = False

    # request from api
    if 'version' in event and event['version'] == "2.0" and 'body' in event:
        if len(event['body'].split(',')) == 2:
            numbers = event['body'].split(',')
            num1 = numbers[0]
            num2 = numbers[1]
        else:
            num1 = 0
            num2 = 0

    try:
        result = float(num1) + float(num2)
        try:
            result = int(result)
        except ValueError:
            pass
    except ValueError as E:
        message = f'Invalid Characters sent, {E}'
        result = False

    if snsMessage and result:
        message = snsMessage + f"\nThe sum is {str(result)}"
    elif result:
        message = f"The sum is {str(result)}"

    sns.publish(TopicArn=topic_arn, Message=message, )

    return {
        'statusCode': 200,
        'body': message
    }

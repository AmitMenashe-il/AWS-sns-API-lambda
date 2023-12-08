# the goal of this project is to gain and maintain knowledge, though not in use - the function logic is viable.

# from aws_lambda_funcs.py
# lambda destination sends the json.dumps(event) into topic, not as intended - instead publishing directly to sns topic from code
'''
def set_lambda_destination(lambda_arn:str, topic_arn:str):
    client = boto3.client('lambda')
    with open('destination_config.json', 'r') as file:
        destination_config = json.load(file)
    # Replace placeholder in json with the actual topic ARN
    destination_config['OnSuccess']['Destination'] = topic_arn
    client.put_function_event_invoke_config(FunctionName=lambda_arn,DestinationConfig=destination_config)
    print(f'lambda granted access to send via topic {topic_arn}')
'''
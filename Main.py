import time
from aws_sns_funcs import create_sns_topic, create_sns_subscription, check_sns_protocol_subscribed, check_sns_topic_existence, get_topic_arn_by_name
from aws_lambda_funcs import create_lambda, get_lambda_function_arn_by_name, delete_lambda_function, check_lambda_exists, create_api_trigger, create_sns_trigger
from api_gw_func import create_api_gateway,  check_api_gateway_id_by_name, get_api_gateway_id_by_name
from aws_IAM_funcs import create_lambda_role_and_assign_policy
from lambda_code_funcs import update_lambda_code_file,create_zip_from_py
from lambda_tests import run_tests


# CODE PART
EMAIL= "amitmenashe@gmail.com"
# topics:
TOPIC_INPUT_NAME = "SNS_Listen"
TOPIC_OUTPUT_NAME = "SNS_Send"
# lambda:
LAMBDA_NAME = "Add_Numbers_Lambda"
LAMBDA_CODE_FILE_NAME = 'handler.py'
LAMBDA_ZIP_FILE_NAME = 'handler.zip'
# api:
API_NAME = "API_number_gw"

# create topics:
print(f'trying to create topic {TOPIC_INPUT_NAME}')
if not check_sns_topic_existence(TOPIC_INPUT_NAME):
    topic_input_arn = create_sns_topic(TOPIC_INPUT_NAME)
else:
    print(f'\ttopic {TOPIC_INPUT_NAME} already exists')
    topic_input_arn = get_topic_arn_by_name(TOPIC_INPUT_NAME)

print(f'trying to create topic {TOPIC_OUTPUT_NAME}')
if not check_sns_topic_existence(TOPIC_OUTPUT_NAME):
    topic_output_arn = create_sns_topic(TOPIC_OUTPUT_NAME)
    print('Recreating lambda file to update destination topic')
    update_lambda_code_file(LAMBDA_CODE_FILE_NAME, topic_output_arn)
    create_zip_from_py(LAMBDA_CODE_FILE_NAME)
    delete_lambda_function(LAMBDA_NAME)
else:
    print(f'\t{TOPIC_OUTPUT_NAME} already exists')
    topic_output_arn = get_topic_arn_by_name(TOPIC_OUTPUT_NAME)

# subscribe email to sns:
print(f'trying to subscribe {EMAIL} to {TOPIC_OUTPUT_NAME}')
if not check_sns_protocol_subscribed(topic_output_arn, "email", EMAIL):
    create_sns_subscription(topic_output_arn, "email", EMAIL)
else:
    print('\t email already subscribed to topic')

# create lambda and policies - has its own try/exceptions:
print(f'trying to create IAM roles and policies:')
lambda_role_arn = create_lambda_role_and_assign_policy(LAMBDA_NAME, topic_output_arn)
# wait for role creation
time.sleep(2)

# create lambda function
print(f'trying to create lambda function {LAMBDA_NAME}')
if not check_lambda_exists(LAMBDA_NAME):
    lambda_arn = create_lambda(LAMBDA_NAME, lambda_role_arn, LAMBDA_ZIP_FILE_NAME)
else:
    print(f'\tlambda function {LAMBDA_NAME} already exists')
    lambda_arn=get_lambda_function_arn_by_name(LAMBDA_NAME)

# register lamda subscription to sns:
print(f'trying to register lambda function {LAMBDA_NAME} to topic {TOPIC_INPUT_NAME} ')
if not check_sns_protocol_subscribed(topic_input_arn, "lambda", lambda_arn):
    create_sns_subscription(topic_input_arn, "lambda", lambda_arn)
else:
    print(f'\tlambda already subscribed to listen to topic {topic_input_arn}')

# create trigger for lambda by sns
print(f'trying to create trigger for  lambda function {LAMBDA_NAME} by topic {TOPIC_INPUT_NAME} ')
create_sns_trigger(LAMBDA_NAME, topic_input_arn)

# create api GW
print(f'trying to create API gateway {API_NAME} ')
if not check_api_gateway_id_by_name(API_NAME):
    api_id = create_api_gateway(API_NAME, LAMBDA_NAME, lambda_arn)
else:
    api_id = get_api_gateway_id_by_name(API_NAME)
    print('\tapi gateway already exists')

print(f'trying to create trigger for  lambda function {LAMBDA_NAME} by api gateway {API_NAME} ')
create_api_trigger(LAMBDA_NAME, api_id)


#tests:
#time to sync for test
#time.sleep(5)
#run_tests(api_id,lambda_name,topic_input_arn)
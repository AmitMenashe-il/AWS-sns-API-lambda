# AWS-sns-API-lambda

uses boto3 python lib
object names are in code part of main.oy (except role and policy names in aws_IAM_funcs.py)
creates:
- a lambda function that recieves 2 numbers and sends their sum to an sns topic (output)
- 2 topics - one for listening(input) and one for publishing(output), listening topic triggers lambda
- subscribes an email to publishing topic
- an api gateway - triggers lambda
- role and policies for lambda
- triggers permissions for sns and api

from aws_sns_funcs import send_sns_message
import os


def api_test(api_id:str,lambda_name:str):
    print('API TEST\n---------------------------')
    print('API Command: curl -X POST -H "Content-Type: application/json" -d "10,20" https://'+api_id+'.execute-api.us-east-1.amazonaws.com/'+lambda_name)
    print('API response: (values Num1=10,Num2=20)')
    os.system('curl -X POST -H "Content-Type: application/json" -d "10,20" https://'+api_id+'.execute-api.us-east-1.amazonaws.com/'+lambda_name)
    print()


def sns_test(topic_input_arn:str):
    print('SNS TEST\n---------------------------')
    print('SNS sent with values 20,40: ')
    sns_res = send_sns_message(topic_input_arn, "40", "20")
    print('SNS Response: ')
    print(sns_res)


def run_tests(api_id:str,lambda_name:str,topic_input_arn:str):
    print('\n')
    sns_test(topic_input_arn)
    print()
    api_test(api_id,lambda_name)

# run_tests('ia4y6p0tk9','Add_Numbers_Lambda','arn:aws:sns:us-east-1:264782567005:SNS_Listen')

# example SNS json from json.dumps(event):
# {
#   "Records": [
#     {
#       "EventSource": "aws:sns",
#       "EventVersion": "1.0",
#       "EventSubscriptionArn": "arn:aws:sns:us-east-1:264782567005:SNS_Listen:c3f62332-0402-4286-92cd-7fe358351936",
#       "Sns": {
#         "Type": "Notification",
#         "MessageId": "464ae2fa-c764-5c99-a774-bf1173b8f526",
#         "TopicArn": "arn:aws:sns:us-east-1:264782567005:SNS_Listen",
#         "Subject": null,
#         "Message": "Message sent by SNS - Sum of Two numbers: 30 and 20",
#         "Timestamp": "2023-12-07T11:55:08.964Z",
#         "SignatureVersion": "1",
#         "Signature": "fOFI35z/AyA/q99LcJvDr9MAjmU24kSQ0VM3wOxw0dWt9inQ9ZlzJcLjqeNV8jfavhKKJmRKkQ+8h34YzFb9hJgIj9VpG6ETrGhmgYw48wdKxUE5XKDZdscPpcszuEKhOL4DhnjecM0PcNgAyeMjH6oQTLg3hov/n0dM0y+QTCF/8Nm3xkR8ciRuCY4kthyz/iPIt8B5/OiWRZepsGDAaYQQ2kohT9ATuP4fgPyJ99z0O+yB/6QIMuDjhhKfeY8mbACTYjb6xIL58+Qq039VTXMTXVc7MwJkxDIAGLu67W1E6Z9gLGBauwQ3F7JOhBOjF6pliGsHUii1YpYkfd/V7A==",
#         "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-01d088a6f77103d0fe307c0069e40ed6.pem",
#         "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:264782567005:SNS_Listen:c3f62332-0402-4286-92cd-7fe358351936",
#         "MessageAttributes": {
#           "Num2": {
#             "Type": "String",
#             "Value": "20.0"
#           },
#           "Num1": {
#             "Type": "String",
#             "Value": "30.0"
#           }
#         }
#       }
#     }
#   ]
# }

# example API json from json.dumps(event):
# {
#   "version": "2.0",
#   "routeKey": "POST /Add_Numbers_Lambda",
#   "rawPath": "/Add_Numbers_Lambda",
#   "rawQueryString": "",
#   "headers": {
#     "accept": "*/*",
#     "content-length": "19",
#     "content-type": "application/json",
#     "host": "ia4y6p0tk9.execute-api.us-east-1.amazonaws.com",
#     "user-agent": "curl/8.4.0",
#     "x-amzn-trace-id": "Root=1-6571b29d-113702a902339af6380f6bfd",
#     "x-forwarded-for": "84.229.134.119",
#     "x-forwarded-port": "443",
#     "x-forwarded-proto": "https"
#   },
#   "requestContext": {
#     "accountId": "264782567005",
#     "apiId": "ia4y6p0tk9",
#     "domainName": "ia4y6p0tk9.execute-api.us-east-1.amazonaws.com",
#     "domainPrefix": "ia4y6p0tk9",
#     "http": {
#       "method": "POST",
#       "path": "/Add_Numbers_Lambda",
#       "protocol": "HTTP/1.1",
#       "sourceIp": "84.229.134.119",
#       "userAgent": "curl/8.4.0"
#     },
#     "requestId": "PkjYrgswoAMEJuA=",
#     "routeKey": "POST /Add_Numbers_Lambda",
#     "stage": "$default",
#     "time": "07/Dec/2023:11:55:09 +0000",
#     "timeEpoch": 1701950109690
#   },
#   "body": "10,20",
#   "isBase64Encoded": false
# }

import boto3,json,time
from datetime import datetime, timedelta

s3 = boto3.client('s3')
RESULT_OUTPUT_LOCATION = "s3://energas-datalake/athenadb/queries/"

def lambda_handler(event, context):
    print("Event: ", event)
    print("Context: ", context)

    body = json.loads(event["body"])
    print("Body: ", body)
    endpoint = body['endpoint']
    print("Endpoint: ", endpoint)
    data_endpoint = body['data']
    print("Data Endpoint: ", data_endpoint)
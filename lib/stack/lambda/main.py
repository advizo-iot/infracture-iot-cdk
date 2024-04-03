import boto3
import json 
from datetime import datetime, timedelta
import time

s3 = boto3.client('s3')
RESULT_OUTPUT_LOCATION = "s3://energas-datalake/athenadb/queries/"

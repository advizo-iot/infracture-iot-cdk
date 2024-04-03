
import time, boto3, base64

def athenaQuery(client,query,location):
    print("Init [athenaQuery]") 
    response = client.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": location}
    )

    return response["QueryExecutionId"]

def waitQueryExecution(client,queryID):
  print("Init [waitQueryExecution]")
  query_status = idStatus(client,queryID)
  while query_status in ['QUEUED', 'RUNNING']:
    query_status = idStatus(client,queryID)
    print(f'Query status: {query_status}')
    if query_status == 'QUEUED' or query_status == 'RUNNING':
        print('Query still running...')
        time.sleep(3)
    else:
        print('Query finished!')
        break

  return client.get_query_results(QueryExecutionId=queryID)

def idStatus(client,queryID):
  response = client.get_query_execution(
        QueryExecutionId=queryID
    )
  print(f"Query status: {response['QueryExecution']['Status']['State']} [idStatus]")
  return response['QueryExecution']['Status']['State']

def download_image_from_s3(url):

    bucket_name = url.split('/')[2]
    object_key = '/'.join(url.split('/')[3:])
    
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response['Body'].read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    # print("Image downloaded from s3")
    # print(f"Image base64: {image_base64}")
    
    return image_base64
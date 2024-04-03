
import time

def athenaQuery(client,query,location):
    print("Init [athenaQuery]") 
    response = client.start_query_execution(
        QueryString=query,
        ResultConfiguration={"OutputLocation": location}
    )

    return response["QueryExecutionId"]

def waitQueryExecution(client,queryID):
  query_status = None
  while query_status == 'QUEUED' or query_status == 'RUNNING':
    response = client.get_query_execution(
        QueryExecutionId=queryID
    )
    query_status = response['QueryExecution']['Status']['State']
    if query_status == 'QUEUED' or query_status == 'RUNNING':
        print('Query still running...')
        time.sleep(3)
    else:
        print('Query finished!')

  return client.get_query_results(QueryExecutionId=queryID)
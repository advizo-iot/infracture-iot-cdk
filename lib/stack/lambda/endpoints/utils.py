
import time

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
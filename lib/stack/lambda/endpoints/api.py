from endpoints.select_query import query_select_users
from endpoints.utils import athenaQuery,waitQueryExecution
import boto3

class apiGatewayIOT:
    def loginIotApp(self,data,location):
        athena_client = boto3.client('athena')

        print(f"Data: {data} [loginIotApp][apiGatewayIOT]")
        query = query_select_users(data['username'],data['password'])
        print(f"Query: {query} [loginIotApp][apiGatewayIOT]")
        queryID = athenaQuery(athena_client,query,location)
        resultQuery = waitQueryExecution(athena_client,queryID)
        print(f"Result: {resultQuery} [loginIotApp][apiGatewayIOT]")

from endpoints.select_query import query_select_users,query_get_map
from endpoints.utils import athenaQuery,waitQueryExecution
import boto3,json

class apiGatewayIOT:
    def loginIotApp(self,data,location):
        athena_client = boto3.client('athena')

        print(f"Data: {data} [loginIotApp][apiGatewayIOT]")
        query = query_select_users(data['username'],data['password'])
        print(f"Query: {query} [loginIotApp][apiGatewayIOT]")
        queryID = athenaQuery(athena_client,query,location)
        resultQuery = waitQueryExecution(athena_client,queryID) 
        print(f"Result: {resultQuery['ResultSet']['Rows']} [loginIotApp][apiGatewayIOT]")

        resultDict = {'dni': None, 'name': None, 'status': 'nok'}
        for row in resultQuery['ResultSet']['Rows']:
            rowData = row['Data']
            if rowData[0]['VarCharValue'] == 'dni':
                continue
            dni = rowData[0]['VarCharValue']
            name = rowData[1]['VarCharValue']
            resultDict['dni'] = dni
            resultDict['name'] = name
            resultDict['status'] = 'ok'

        resultJSON = json.dumps(resultDict)
        print(f"Result JSON: {resultJSON}")

        return resultJSON
    
    def getMapUser(self,data,location):
        athena_client = boto3.client('athena')

        print(f"Data: {data} [getMapUser][apiGatewayIOT]")
        query = query_get_map(data['dni'])
        print(f"Query: {query} [getMapUser][apiGatewayIOT]")
        queryID = athenaQuery(athena_client,query,location)
        resultQuery = waitQueryExecution(athena_client,queryID) 
        print(f"Result: {resultQuery['ResultSet']['Rows']} [getMapUser][apiGatewayIOT]")
        resultDict = {'map_id': None, 'url_map': None, 'status': 'nok'}

        resultJSON = json.dumps(resultDict)
        print(f"Result JSON: {resultJSON}")

        return resultJSON
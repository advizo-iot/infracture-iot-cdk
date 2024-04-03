from endpoints.select_query import query_select_users,query_get_map,query_get_coordenates
from endpoints.utils import athenaQuery,waitQueryExecution,download_image_from_s3
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
        resultDict = {'dni': None, 'map_id': None, 'url_map': None, 'status': 'nok'}

        for row in resultQuery['ResultSet']['Rows']:
            rowData = row['Data']
            if rowData[0]['VarCharValue'] == 'dni':
                continue
            dni = rowData[0]['VarCharValue']
            map_id = rowData[1]['VarCharValue']
            url_map = rowData[2]['VarCharValue']
            resultDict['dni'] = dni
            resultDict['map_id'] = map_id
            download_image_from_s3(url_map)
            resultDict['url_map'] = url_map
            resultDict['status'] = 'ok'

        resultJSON = json.dumps(resultDict)
        print(f"Result JSON: {resultJSON}")

        return resultJSON
    
    def getMapCoordenates(self,data,location):
        athena_client = boto3.client('athena')

        print(f"Data: {data} [getMapCoordenates][apiGatewayIOT]")
        query = query_get_coordenates(data['dni'],data['map_id'])
        print(f"Query: {query} [getMapCoordenates][apiGatewayIOT]")
        queryID = athenaQuery(athena_client,query,location)
        resultQuery = waitQueryExecution(athena_client,queryID)
        print(f"Result: {resultQuery['ResultSet']['Rows']} [getMapCoordenates][apiGatewayIOT]")
        resultDict = {'data': []}

        for row in resultQuery['ResultSet']['Rows']:
            rowData = row['Data']
            print(f"Row Data: {rowData}")
            if rowData[0]['VarCharValue'] == 'dni':
                continue
            
            dni = rowData[0]['VarCharValue']
            map_id = rowData[1]['VarCharValue']
            sensor_id = rowData[2]['VarCharValue']
            coordenates = rowData[3]['VarCharValue']
            coordinates_str = coordenates.strip("{ }").split(", ")
            x_value = float(coordinates_str[0].split(":")[1].strip())
            y_value = float(coordinates_str[1].split(":")[1].strip())
            coordinates = {"x": x_value, "y": y_value}

            resultDict['data'].append({
                'dni': dni,
                'map_id': map_id,
                'sensor_id': sensor_id,
                'coordinates': coordinates
            })

        resultJSON = json.dumps(resultDict)
        print(f"Result JSON: {resultJSON}")

        return resultJSON
        
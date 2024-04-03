from select_query import query_select_users

class apiGatewayIOT:
    def loginIotApp(self,data):
        print(f"Data: {data} [loginIotApp][apiGatewayIOT]")
        query = query_select_users(data['username'],data['password'])
        print(f"Query: {query} [loginIotApp][apiGatewayIOT]")
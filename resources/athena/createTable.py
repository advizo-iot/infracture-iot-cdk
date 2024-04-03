import boto3, time, os
CLIENT = boto3.client("athena")
DATABASE_NAME = "production_raw_iot_advizo"
RESULT_OUTPUT_LOCATION = "s3://advizo-iot-fire-resources/athenadb/queries/"
CATALOG_NAME = "AWSDataCatalog"
ddl_file = "ddl/map_factory.ddl"

def has_query_succeeded(execution_id):
    state = "RUNNING"
    max_execution = 5

    while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
        max_execution -= 1
        response = CLIENT.get_query_execution(QueryExecutionId=execution_id)
        if (
            "QueryExecution" in response
            and "Status" in response["QueryExecution"]
            and "State" in response["QueryExecution"]["Status"]
        ):
            state = response["QueryExecution"]["Status"]["State"]
            if state == "SUCCEEDED":
                return True

        time.sleep(5)

    return False

def create_table(TABLE_DDL_TABLE):
    table_name = TABLE_DDL_TABLE.split("/")[-1].split(".")[0]
    print(f"Creating table '{table_name}' in database '{DATABASE_NAME}'")
    tables = CLIENT.list_table_metadata(CatalogName=CATALOG_NAME,DatabaseName=DATABASE_NAME)
    existing_tables = [table["Name"] for table in tables["TableMetadataList"]]
    if table_name in existing_tables:
        print(f"Table '{table_name}' already exists in database '{DATABASE_NAME}'. Skipping table creation.")
        return None

    with open(TABLE_DDL_TABLE) as ddl:
        response = CLIENT.start_query_execution(
            QueryString=ddl.read(),
            ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION}
        )

        return response["QueryExecutionId"]
    
def main():
  script_dir = os.path.dirname(os.path.abspath(__file__))
  ddl_file_path = os.path.join(script_dir, ddl_file)
  print(f"DDL file path: {ddl_file_path}")
  execution_id = create_table(ddl_file_path)
  if execution_id is None:
    return
  print(f"Create Table users execution id: {execution_id}")
  query_status = has_query_succeeded(execution_id=execution_id)
  print(f"Query state: {query_status}")

if __name__ == "__main__":
    main()
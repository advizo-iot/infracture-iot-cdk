import boto3, time
CLIENT = boto3.client("athena")
DATABASE_NAME = "production_raw_iot_advizo"
RESULT_OUTPUT_LOCATION = "s3://advizo-iot-fire-resources/athenadb/queries/"


def create_database():
    databases = CLIENT.list_databases()
    existing_databases = [db["Name"] for db in databases["DatabaseList"]]

    if DATABASE_NAME not in existing_databases:
        print(f"Creating database '{DATABASE_NAME}' [create_database]")
        response = CLIENT.start_query_execution(
            QueryString=f"create database {DATABASE_NAME}",
            ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION}
        )

        return response["QueryExecutionId"]
    else:
        print(f"Database '{DATABASE_NAME}' already exists. [create_database]")

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

def main():
    execution_id = create_database()
    print(f"Checking query execution for: {execution_id}")
    query_status = has_query_succeeded(execution_id=execution_id)
    print(f"Query status: {query_status}")

if __name__ == "__main__":
    main()
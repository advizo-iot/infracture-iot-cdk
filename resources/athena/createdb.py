import boto3
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

def main():
    create_database()

if __name__ == "__main__":
    main()
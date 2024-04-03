import boto3
CLIENT = boto3.client("athena")
DATABASE_NAME = "production_stage_energas"
RESULT_OUTPUT_LOCATION = "s3://energas-datalake/athenadb/queries/"


def create_database():
    response = CLIENT.start_query_execution(
        QueryString=f"create database {DATABASE_NAME}",
        ResultConfiguration={"OutputLocation": RESULT_OUTPUT_LOCATION}
    )

    return response["QueryExecutionId"]
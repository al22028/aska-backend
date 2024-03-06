# mypy: ignore-errors

import boto3
import json


client = boto3.client("lambda")


def invoke_lambda():
    payload = {"body": "Hello world"}

    response = client.invoke(
        FunctionName="aska-api-dev-InvokedLambdaHandler",
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=bytes(json.dumps(payload).encode()),
    )
    print(response["Payload"].read().decode("utf-8"))


if __name__ == "__main__":
    invoke_lambda()

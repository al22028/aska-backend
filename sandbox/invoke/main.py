# mypy: ignore-errors

import boto3


client = boto3.client("lambda")


def invoke_lambda():
    response = client.invoke(
        FunctionName="aska-api-dev-MatchingCalculatHandler",
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=b'{"body": "hello"}',
    )
    print(response["Payload"].read().decode("utf-8"))


if __name__ == "__main__":
    invoke_lambda()

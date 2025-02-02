# Standard Library
import json

# Third Party Library
import boto3
from schemas.payload import LambdaInvokePayload


class LambdaClient:
    client = boto3.client("lambda")

    def invoke(self, function_name: str, payload: LambdaInvokePayload) -> str:
        """Invoke Lambda functionS

        Args:
            function_name (str): function name
            payload (LambdaInvokePayload): payload

        Returns:
            tuple[str, int]: Payload and StatusCode
        """
        response = self.client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=bytes(json.dumps(payload.model_dump()).encode()),
        )
        return response["Payload"].read().decode("utf-8")

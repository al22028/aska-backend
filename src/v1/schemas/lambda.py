# Third Party Library
from pydantic import BaseModel


class LambdaInvokePayload(BaseModel):
    body: dict

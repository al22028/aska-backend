# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel

tracer = Tracer()
logger = Logger()

app = APIGatewayRestResolver()
app.enable_swagger(path="/swagger", title="Aska API")


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict[str, str | int]:
    return app.resolve(event, context)


class HealthCheckSchema(BaseModel):
    status: str


@app.get("/healthcheck")
def health_check(event: dict, context: LambdaContext) -> HealthCheckSchema:
    return HealthCheckSchema(**{"status": "ok"})

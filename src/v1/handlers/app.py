# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.openapi.models import Server
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, Field
from routes import user

tracer = Tracer()
logger = Logger()

app = APIGatewayRestResolver(enable_validation=True)
app.enable_swagger(
    path="/swagger",
    title="Aska API",
    servers=[
        Server(url="http://localhost:3333", description="Local Development Server", variables=None),
    ],
)

app.include_router(user.router, prefix="/v1/users")


class HealthCheckSchema(BaseModel):
    status: str = Field(..., description="Health Check Status", example="ok")


@app.get(
    "/healthcheck",
    cors=True,
    summary="Health Check",
    response_description="Health Check",
    tags=["default"],
    operation_id="healthcheck",
)
def health_check() -> HealthCheckSchema:
    return HealthCheckSchema(**{"status": "ok"})


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict[str, str | int]:
    return app.resolve(event, context)

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.openapi.models import Server
from aws_lambda_powertools.utilities.typing import LambdaContext
from config.settings import STAGE
from middlewares.common import handler_middleware
from pydantic import BaseModel, Field
from routes import dev, image, json, page, project, user, version

tracer = Tracer()
logger = Logger()


if STAGE == "local":
    servers = [
        Server(url="http://localhost:3333", description="Local Development Server", variables=None),
    ]
elif STAGE == "dev":
    servers = [
        Server(
            url="https://api-dev.u10.teba-saki.net",
            description="Development Server",
            variables=None,
        ),
    ]
else:
    servers = [
        Server(
            url="https://api-dev.u10.teba-saki.net",
            description="Development Server",
            variables=None,
        ),
        Server(url="http://localhost:3333", description="Local Development Server", variables=None),
    ]

app = APIGatewayRestResolver(enable_validation=True)
app.enable_swagger(
    path="/swagger",
    title="Aska API",
    servers=servers,
)

app.include_router(user.router, prefix="/users")
app.include_router(project.router, prefix="/projects")
app.include_router(version.router, prefix="/versions")
app.include_router(page.router, prefix="/pages")
app.include_router(image.router, prefix="/images")
app.include_router(json.router, prefix="/jsons")

if STAGE != "prod":
    app.include_router(dev.router, prefix="/dev")


class HealthCheckSchema(BaseModel):
    status: str = Field(..., description="Health Check Status", example="ok")  # type: ignore


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


@handler_middleware
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict[str, str | int]:
    return app.resolve(event, context)

# Third Party Library
from config import settings


def test_aws_region() -> None:
    assert settings.AWS_REGION == "ap-northeast-1"


def test_stage() -> None:
    assert settings.STAGE == "dev"


def test_app_api_version() -> None:
    assert settings.APP_API_VERSION == "v1"


def test_app_api_cors_allowed_origins() -> None:
    assert settings.APP_API_CORS_ALLOWED_ORIGINS is not None


def test_aws_rds_database_url() -> None:
    assert settings.AWS_RDS_DATABASE_URL == "postgresql+psycopg2://aska:aska@localhost:5433/app"


def test_sqlalchemy_echo_sql() -> None:
    assert settings.SQLALCHEMY_ECHO_SQL is False

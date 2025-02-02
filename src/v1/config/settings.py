# Third Party Library
from decouple import config

AWS_REGION = config("AWS_REGION", default="ap-northeast-1", cast=str)
STAGE = config("STAGE", default="dev", cast=str)

# api config
APP_API_VERSION = config("APP_API_VERSION", default="v1", cast=str)
APP_API_CORS_ALLOWED_ORIGINS: str = config("APP_API_CORS_ALLOWED_ORIGINS", default="*", cast=str)
APP_API_CORS_ALLOWED_ORIGIN_LIST: list[str] = APP_API_CORS_ALLOWED_ORIGINS.split(",")

# powertools config
POWERTOOLS_DEBUG = config("POWERTOOLS_DEBUG", default=False, cast=bool)

# database config
AWS_RDS_DATABASE_URL = config(
    "AWS_RDS_DATABASE_URL",
    default="postgresql+psycopg2://aska:aska@localhost:5433/app",
    cast=str,
)
SQLALCHEMY_ECHO_SQL = config("SQLALCHEMY_ECHO_SQL", default=False, cast=bool)

# AWS S3
AWS_PDF_BUCKET = config("AWS_PDF_BUCKET", default="aska-pdf-bucket-dev", cast=str)
AWS_IMAGE_BUCKET = config("AWS_IMAGE_BUCKET", default="aska-image-bucket-dev", cast=str)
AWS_TMP_BUCKET = config("AWS_TMP_BUCKET", default="aska-tmp-bucket-dev", cast=str)

# AWS CloudFront
AWS_IMAGE_HOST_DOMAIN = config(
    "AWS_IMAGE_HOST_DOMAIN", default="https://d3jn185gjojza6.cloudfront.net/", cast=str
)

# AWS Cognito
AWS_COGNITO_USER_POOL_ID = config("AWS_COGNITO_USER_POOL_ID", default="", cast=str)
AWS_COGNITO_CLIENT_ID = config("AWS_COGNITO_CLIENT_ID", default="", cast=str)

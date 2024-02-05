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
    default="postgresql+psycopg2://psaco:psaco@localhost:5433/app",
    cast=str,
)
SQLALCHEMY_ECHO_SQL = config("SQLALCHEMY_ECHO_SQL", default=False, cast=bool)

# AWS S3 config
AWS_POSTER_ASSETS_BUCKET_NAME = config(
    "AWS_POSTER_ASSETS_BUCKET_NAME", default="psaco-poster-assets-bucket-dev", cast=str
)
AWS_USER_PROFILE_IMAGE_BUCKET_NAME = config(
    "AWS_USER_PROFILE_IMAGE_BUCKET_NAME", default="psaco-user-profile-image-bucket-dev", cast=str
)
AWS_USER_PROFILE_HOSTING_DOMAIN = config(
    "AWS_USER_PROFILE_HOSTING_DOMAIN",
    default="https://dg5h3h03scc10.cloudfront.net",
    cast=str,
)

AWS_POSTER_THUMBNAIL_BUCKET_NAME = config(
    "AWS_POSTER_THUMBNAIL_BUCKET_NAME", default="psaco-poster-thumbnail-bucket", cast=str
)

AWS_POSTER_THUMBNAIL_HOSTING_DOMAIN = config(
    "AWS_POSTER_THUMBNAIL_HOSTING_DOMAIN",
    default="https://psaco-poster-thumbnail-bucket.s3.ap-northeast-1.amazonaws.com",
    cast=str,
)

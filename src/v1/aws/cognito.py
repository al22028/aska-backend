# Third Party Library
import boto3
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from config.settings import AWS_COGNITO_CLIENT_ID, AWS_COGNITO_USER_POOL_ID
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from mypy_boto3_cognito_idp.type_defs import (
    AdminCreateUserResponseTypeDef,
    AdminInitiateAuthResponseTypeDef,
    AdminRespondToAuthChallengeResponseTypeDef,
)


class Cognito:
    client: CognitoIdentityProviderClient = boto3.client("cognito-idp")

    def __init__(self) -> None:
        self._user_pool_id = AWS_COGNITO_USER_POOL_ID
        self._client_id = AWS_COGNITO_CLIENT_ID

    def create_user(self, email: str, password: str) -> str:
        response: AdminCreateUserResponseTypeDef = self.client.admin_create_user(
            UserPoolId=self._user_pool_id,
            Username=email,
            UserAttributes=[{"Name": "email", "Value": email}],
            TemporaryPassword=password,
            MessageAction="SUPPRESS",
        )
        user_id = None
        attributes = response["User"]["Attributes"]
        for attribute in attributes:
            if attribute["Name"] == "sub":
                user_id = attribute["Value"]
                break
        if not user_id:
            raise BadRequestError("user id not found")
        return user_id

    def confirm_user(self, email: str, password: str) -> AdminRespondToAuthChallengeResponseTypeDef:
        _response: AdminInitiateAuthResponseTypeDef = self.client.admin_initiate_auth(
            UserPoolId=self._user_pool_id,
            ClientId=self._client_id,
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
        session = _response["Session"]
        response: AdminRespondToAuthChallengeResponseTypeDef = (
            self.client.admin_respond_to_auth_challenge(
                UserPoolId=self._user_pool_id,
                ClientId=self._client_id,
                ChallengeName="NEW_PASSWORD_REQUIRED",
                ChallengeResponses={"USERNAME": email, "NEW_PASSWORD": password},
                Session=session,
            )
        )
        return response

    def verify_email(self, email: str) -> dict:
        """Verify email

        Args:
            email (str): user email

        Returns:
            dict: updated user attributes response
        """
        response = self.client.admin_update_user_attributes(
            UserPoolId=self._user_pool_id,
            Username=email,
            UserAttributes=[{"Name": "email_verified", "Value": "true"}],
        )
        return response

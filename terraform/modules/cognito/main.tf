resource "aws_cognito_user_pool" "client" {
  name = "aska-user-pool"
  auto_verified_attributes = [
    "email",
  ]

  # sign up configuration
  username_attributes = ["email"]

  # email configuration
  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }
  # required attributes for sign up (email)
  schema {
    attribute_data_type = "String"
    name                = "email"
    required            = true
  }

  # password policy
  password_policy {
    minimum_length                   = 6
    require_lowercase                = false
    require_numbers                  = true
    temporary_password_validity_days = 30
  }
  # MFAs are not required for this project
  mfa_configuration = "OFF"


  user_attribute_update_settings {
    attributes_require_verification_before_update = ["email"]
  }

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  # delete protection
  deletion_protection = "INACTIVE"

  tags = {
    Service = "psaco"
    Env     = "dev"
  }
}

resource "aws_cognito_user_pool_client" "client" {
  name                = "psaco-user-pool-client"
  user_pool_id        = aws_cognito_user_pool.client.id
  generate_secret     = false
  explicit_auth_flows = ["ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_SRP_AUTH"]
}

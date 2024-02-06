terraform {
  # asdf terraform version 1.6.6
  required_version = "1.6.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.30.0"
    }
  }

  backend "s3" {
    bucket = "aska-iac-terraform-backend-bucket"
    key    = "dev/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "ap-northeast-1"
}

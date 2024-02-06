locals {
  public_subnet_args = {
    "ap-northeast-1a" = "10.0.0.0/20"
    "ap-northeast-1c" = "10.0.16.0/20"
  }
  private_subnet_args = {
    "ap-northeast-1a" = "10.0.128.0/20"
    "ap-northeast-1c" = "10.0.144.0/20"
  }
}

# VPC
resource "aws_vpc" "this" {
  cidr_block           = "10.0.0.0/16"
  instance_tenancy     = "default"
  enable_dns_hostnames = true
  tags = {
    Name = "app-vpc-${var.suffix}"
  }
}

# Public Subnet
resource "aws_subnet" "public" {
  for_each = local.public_subnet_args

  vpc_id            = aws_vpc.this.id
  availability_zone = each.key
  cidr_block        = each.value
  tags = {
    Name = "app-public-subnet-${each.key}-${var.suffix}"
  }
}

# Private Subnet
resource "aws_subnet" "private" {
  for_each = local.private_subnet_args

  vpc_id            = aws_vpc.this.id
  availability_zone = each.key
  cidr_block        = each.value
  tags = {
    Name = "app-private-subnet-${each.key}-${var.suffix}"
  }
}
resource "aws_eip" "nat_gateway" {
  domain = "vpc"
  tags = {
    Name = "app-eip-for-nat-gateway-${var.suffix}"
  }
}

resource "aws_nat_gateway" "this" {
  allocation_id = aws_eip.nat_gateway.id
  subnet_id     = aws_subnet.public["ap-northeast-1a"].id
  tags = {
    Name = "app-nat-gateway-${var.suffix}"
  }
  depends_on = [aws_internet_gateway.this]
}

# Internet Gateway
resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
  tags = {
    Name = "app-igw-${var.suffix}"
  }
}


# Default Route Table
resource "aws_default_route_table" "default" {
  default_route_table_id = aws_vpc.this.default_route_table_id
  route                  = []
  tags = {
    Name = "app-rtb-default-${var.suffix}"
  }
}

# Route Table for Public Subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }
  tags = {
    Name = "app-rtb-public-${var.suffix}"
  }
}


# Route Table for Private Subnet
resource "aws_route_table" "private1a" {
  vpc_id = aws_vpc.this.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.this.id
  }
  tags = {
    Name = "app-rtb-private1a-${var.suffix}"
  }
}

# Route Table for Private Subnet
resource "aws_route_table" "private1c" {
  vpc_id = aws_vpc.this.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.this.id
  }
  tags = {
    Name = "app-rtb-private1c-${var.suffix}"
  }
}

# Associate Route Table to Public Subnet
resource "aws_route_table_association" "public1a" {
  subnet_id      = aws_subnet.public["ap-northeast-1a"].id
  route_table_id = aws_route_table.public.id
}

# Associate Route Table to Public Subnet
resource "aws_route_table_association" "public1c" {
  subnet_id      = aws_subnet.public["ap-northeast-1c"].id
  route_table_id = aws_route_table.public.id
}

# Associate Route Table to Private Subnet
resource "aws_route_table_association" "private1a" {
  subnet_id      = aws_subnet.private["ap-northeast-1a"].id
  route_table_id = aws_route_table.private1a.id
}

# Associate Route Table to Private Subnet
resource "aws_route_table_association" "private1c" {
  subnet_id      = aws_subnet.private["ap-northeast-1c"].id
  route_table_id = aws_route_table.private1c.id
}

# VPC Endpoint for S3
resource "aws_vpc_endpoint" "s3" {
  vpc_id          = aws_vpc.this.id
  service_name    = "com.amazonaws.ap-northeast-1.s3"
  route_table_ids = [aws_route_table.private1a.id, aws_route_table.private1c.id]
  tags = {
    Name = "app-vpc-endpoint-s3-${var.suffix}"
  }
}

# Security Group for Postgres
resource "aws_security_group" "allow_postgres" {
  name        = "allow-postgres"
  description = "Allow Postgres"
  vpc_id      = aws_vpc.this.id
  ingress {
    description = "Postgres"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  tags = {
    Name = "allow-postgres-${var.suffix}"
  }
}

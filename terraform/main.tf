# initialising terraform providers and aws region (to apply before adding the included backend s3 block)
terraform {
  required_providers {
    aws ={
        source  = "hashicorp/aws"
        version = "~> 5.100.0"
    }
  }

  backend "s3" {
    bucket         = "gdpr-terraform-state-bucket" # Replace with your bucket name
    key            = "terraform/.terraform/terraform.tfstate" # Define the path for the state file
    region         = "eu-west-2"                # Match your bucket's region
    encrypt        = true
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
        ProjectName  = "GDPR Obfuscator"
        Team         = "tech-returners"
        DeployedFrom = "Terraform"
        Repository   = "gdpr-project"
        Enviroment   = "dev"
    }
  }
}


# Assigning iam role
resource "aws_iam_role" "lambda_role" {
  name               = "lambda_execution_role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Attaching iam policy
resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_policy"
  description = "Policy for Lambda execution"
  policy      = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:logs:eu-west-2:910599466119:log-group:/aws/lambda/obfuscator_lambda:*"
      },
      {
        "Sid": "StatementInput",
        "Effect": "Allow",
        "Action": [
            "s3:GetObject",
            "s3:GetObjectAcl",
            "s3:ListBucket"
        ],
        "Resource": [
            "arn:aws:s3:::gdpr-data-storage",
            "arn:aws:s3:::gdpr-data-storage/*"
        ]
      },
      {
        "Sid": "StatementOutput",
        "Effect": "Allow",
        "Action": [
            "s3:PutObject",
            "s3:PutObjectAcl"
        ],
        "Resource": [
            "arn:aws:s3:::gdpr-obfuscator-ouput",
            "arn:aws:s3:::gdpr-obfuscator-ouput/*"
        ]
      },
      {
        "Sid": "Statement1",
        "Effect": "Allow",
        "Action": [
            "s3:GetBucketPolicy"
        ],
        "Resource": [
            "arn:aws:s3:::gdpr-obfuscator-ouput/*",
            "arn:aws:s3:::gdpr-data-storage/*"
        ]
      }
    ]
  })
}

# Attaching lambda role policy
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Creating a lambda handler with zipped dependencies
resource "aws_lambda_function" "lambda_handler" {
  role          = aws_iam_role.lambda_role.arn
  function_name = "lambda_handler"
  
  # handler = "python_module.function_in_the_module"
  handler       = "lambda_handler.lambda_handler"
  
  runtime       = "python3.12"
  filename      = "${path.module}/my_deployment_package.zip"
  source_code_hash = filebase64sha256("my_deployment_package.zip")
}

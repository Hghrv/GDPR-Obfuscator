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
        Team         = "Tech-Returners"
        DeployedFrom = "Terraform"
        Repository   = "GDPR-Project"
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
        Resource = [
          "arn:aws:lambda:eu-west-2:910599466119:function:*",
          "arn:aws:logs:eu-west-2:910599466119:log-group:*"
        ]
      },
      {
        "Sid": "StatementInput",
        "Effect": "Allow",
        "Action": ["s3:GetObject"],
        "Resource": [
            "arn:aws:s3:::gdpr-data-storage",
            "arn:aws:s3:::gdpr-data-storage/*"
        ]
      },
      {
        "Sid": "StatementOutput",
        "Effect": "Allow",
        "Action": ["s3:PutObject"],
        "Resource": [
            "arn:aws:s3:::gdpr-obfuscator-ouput",
            "arn:aws:s3:::gdpr-obfuscator-ouput/*"
        ]
      },
      {
        "Sid": "Statement1",
        "Effect": "Allow",
        "Action": ["s3:GetBucketPolicy"],
        "Resource": [
            "arn:aws:s3:::gdpr-obfuscator-ouput/*",
            "arn:aws:s3:::gdpr-data-storage/*"
        ]
      },
      {
        "Sid": "Statement2",
        "Effect": "Allow",
        "Action": "events:PutEvents",
        "Resource": "*"
      }
    ]
  })
}

# Attaching lambda role policy
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Provisioning lambda_handler.py with zipped dependencies
resource "aws_lambda_function" "lambda_handler" {
  role             = aws_iam_role.lambda_role.arn
  function_name    = "lambda_handler"
  
  # handler        = "python_module.function_in_the_module"
  handler          = "lambda_handler.lambda_handler"
  
  runtime          = "python3.12"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}

# Defining archive_file for zip paths
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/src/lambda_handler.py"
  output_path = "${path.module}/lambda_function.zip"
}

# Granting lambda permision to be invoked by s3
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_handler.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.gdpr_data_storage.arn
}

# Setting s s3 notification to trigger the lambda function when a new file is uploaded
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = "gdpr_data_storage"
  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda_handler.arn
    events              = ["s3:ObjectCreated:*"]
  }
  depends_on = [
    aws_lambda_permission.allow_s3
  ]
}

# Setting Cloudwatch event rule
resource "aws_cloudwatch_event_rule" "s3_put_object_rule" {
  name        = "s3-put-object-rule"
  description = "Triggers when a new file is uploaded to the S3 bucket"
  event_pattern = <<PATTERN
{
  "source": ["aws.s3"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventSource": ["s3.amazonaws.com"],
    "eventName": ["PutObject"],
    "requestParameters": {
      "bucketName": ["gdpr_data_storage"]
    }
  }
}
PATTERN
}

# Adding Cloudwatch event target
resource "aws_cloudwatch_event_target" "lambda_target" {
   rule     = aws_cloudwatch_event_rule.s3_put_object_rule.name
  target_id = "lambda_target"
  arn       = aws_lambda_function.lambda_handler.arn

  input = jsonencode({
    "file_to_obfuscate" = "new_data/test_file.csv"
    "pii_fields" = ["name", "email_address"]
  })
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_handler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.s3_put_object_rule.arn
}

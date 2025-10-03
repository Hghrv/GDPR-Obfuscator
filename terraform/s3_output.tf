# Creating output s3 bucket
resource "aws_s3_bucket" "gdpr-obfuscator-ouput" {
    bucket = "gdpr-obfuscator-ouput"
    tags = {
        Name = "gdpr output bucket"
    }
    force_destroy = true
}

# Attaching bucket policy
resource "aws_iam_policy" "policy" {
  name        = "BucketAccessPolicy"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::910599466119:role/service-role/obfuscator_lambda-role-rflt62d9"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::gdpr-obfuscator-ouput/*"
        }
    ]
}
EOF
}
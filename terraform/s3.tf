# Creating input s3 bucket
resource "aws_s3_bucket" "gdpr_data_storage" {
    bucket = "gdpr-data-storage"
    tags = {
        Name = "gdpr obfuscator bucket"
    }
    force_destroy = true
}


# Attaching bucket policy
resource "aws_iam_policy" "bucket-policy" {
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
                "s3:GetObject"                
            ],
            "Resource": [
                "arn:aws:s3:::gdpr-data-storage",
                "arn:aws:s3:::gdpr-data-storage/*"
            ]
        }
    ]
}
EOF
}

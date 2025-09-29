resource "aws_s3_bucket" "gdpr_data_storage" {
    bucket = "gdpr-data-storage"
    tags = {
        Name = "gdpr obfuscator bucket"
    }
    force_destroy = true
}

resource "aws_iam_policy" "policy" {
  name        = "BucketAccessPolicy"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "${aws_s3_bucket.gdpr_data_storage.arn}",
        "${aws_s3_bucket.gdpr_data_storage.arn}/*"
      ]
    }
  ]
}
EOF
}
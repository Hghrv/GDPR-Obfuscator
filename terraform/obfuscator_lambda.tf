{
  "Version":"2012-10-17",		 	 	 
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "IngestionStmt",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectAcl",
        "s3:ListBucket",
        "s3:ListBucketAcl"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::gdpr-data-storage"
      ]
    }
  ]
}

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "OutputStmt",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::gdpr-obfuscator-ouput"
      ]
    }
  ]
}
from src import lambda_handler
import logging
import boto3
from moto import mock_aws
import pytest
import botocore.exceptions
from unittest.mock import patch
import pandas as pd

# Setting s3 bucket fixture for mock tests
@pytest.fixture
def mock_s3_bucket():
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-west-2")
        bucket_name = "test-bucket"
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        test_files = ["new_data/test_file.csv", "new_data/test_file.json", "new_data/test_file.pkl"]
        for file in test_files:
            s3.put_object(Bucket=bucket_name, Key=file)

        with open("./new_data/test_file.csv", "rb") as f:
            body = f
            s3.put_object(Bucket=bucket_name, Key="test_file_1.csv", Body=body)

        yield bucket_name

# defining tests
class TestUploadToOuputS3:
    def test_upload_to_ouput_s3(self, mock_s3_bucket):
        pass
from src.utils.upload_to_ouput_s3 import upload_to_ouput_s3
import csv
import os
import logging
# import pandas as pd
# import json
import boto3
from moto import mock_aws
import pytest
import botocore.exceptions
from unittest.mock import patch
from testfixtures import LogCapture

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

        yield bucket_name

# defining tests
class TestUploadToOuputS3:
    def test_upload_to_ouput_s3_returs_dictionary(self, mock_s3_bucket):
        
        bucket_name_output = mock_s3_bucket
        output_key = "obfuscated_data/obfuscated-file.csv"
        file_to_upload = "src/test_file.csv"

        upload_test = upload_to_ouput_s3(bucket_name_output, output_key, file_to_upload)
        # Asserting that the function returns a dictionary
        assert isinstance(upload_test, dict), "response is not a dictionary instance"
        
        response = upload_test["output key"]
        # Asserting whether the file name ends with '.csv' extension
        assert response.endswith('.csv')

    def test_upload_to_ouput_s3(self, mock_s3_bucket):
        
        # s3 = empty_nc_terraformers_ingestion_s3
        # data = json.dumps({"test": "data"})   # for json instance

        output_key = "obfuscated_data/obfuscated-file.csv"
        file_to_upload = "src/test_file.csv"

        response = upload_to_ouput_s3(mock_s3_bucket, output_key, file_to_upload)

        expected_output ="obfuscated_data/obfuscated-file.csv"
        
        s3_client = boto3.client('s3')
        objects = s3_client.list_objects_v2(Bucket = mock_s3_bucket)
        assert objects["Contents"][0]['Key']== expected_output
        assert response["result"] == "Success"

    @mock_aws
    def test_handles_no_such_bucket_error(self):
        s3 = boto3.client("s3")
        # data = json.dumps({"test": "data"})

        with LogCapture() as log:
            output = upload_to_ouput_s3("non-existant-bucket", "obfuscated_data/obfuscated-file.csv", "src/test_file.csv")
            assert output["result"] == "Failure"
            assert ("root ERROR\n  An error occurred (NoSuchBucket) when "
                + "calling the PutObject operation: The specified bucket"
                + " does not exist") in (str(log))

    def test_handles_filename_error(self, mock_s3_bucket):
        
        output_s3 = mock_s3_bucket
        with LogCapture() as log:
            output = upload_to_ouput_s3("{output_s3}", "test-key", "non-existant-file.csv")
            assert output["result"] == "Failure"
            assert "Parameter validation failed:\nInvalid" in str(log)
           

"""
    def test_returns_dict(self, empty_nc_terraformers_ingestion_s3):
        s3 = empty_nc_terraformers_ingestion_s3
        data = json.dumps({"test": "data"})

        bucket_name_output = mock_s3_bucket
        output_key = "obfuscated_data/obfuscated-file.csv"
        file_to_upload = "src/test_file.csv"

        assert isinstance(
            upload_to_ouput_s3(bucket_name_output, output_key, file_to_upload)
            ),
            csv,
        )
    
    def test_upload_to_ouput_s3(self, empty_nc_terraformers_ingestion_s3):
        s3 = empty_nc_terraformers_ingestion_s3
        data = json.dumps({"test": "data"})
        output = write_to_s3(
            s3,
            "nc-terraformers-ingestion-123",
            "test-file",
            "pkl",
            data,
        )
        objects = s3.list_objects(Bucket="nc-terraformers-ingestion-123")
        assert objects["Contents"][0]["Key"] == "test-file.pkl"
        assert output["result"] == "Success"

    @mock_aws
    def test_handles_no_such_bucket_error(self):
        s3 = boto3.client("s3")
        data = json.dumps({"test": "data"})

        with LogCapture() as log:
            output = write_to_s3(
                s3, "non-existant-bucket", "test-file", "pkl", data
                )
            assert output["result"] == "Failure"
            assert (
                "root ERROR\n  An error occurred (NoSuchBucket) when "
                + "calling the PutObject operation: The specified bucket"
                + " does not exist"
                in (str(log))
            )

    def test_handles_filename_error(self, empty_nc_terraformers_ingestion_s3):
        data = True
        s3 = empty_nc_terraformers_ingestion_s3
        with LogCapture() as log:
            output = write_to_s3(s3, "test-bucket", "test-file", "pkl", data)
            assert output["result"] == "Failure"
            assert (
                "root ERROR\n  Parameter validation failed:\nInvalid "
                + "type for parameter Body, value: True, type: <class "
                + "'bool'>, valid types: <class 'bytes'>, <class "
                + "'bytearray'>, file-like object"
                in str(log)
            )
"""
from layer2 import get_data, tranform_file_into_df
import logging
import boto3
from moto import mock_aws
import pytest
import botocore.exceptions
from unittest.mock import patch
import pandas as pd


@pytest.fixture
def mock_s3_bucket():
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-west-2")
        bucket_name = "test-bucket"
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        test_files = ["test.csv", "test.json", "test.pkl"]
        for file in test_files:
            s3.put_object(Bucket=bucket_name, Key=file)

        with open("./test1.csv", "rb") as f:
            body = f
            s3.put_object(Bucket=bucket_name, Key="test1.csv", Body=body)

        yield bucket_name

class TestObfuscatorInput:
    def test_lambda_handler_downloads_csv_files_to_input_s3_bucket(self, mock_s3_bucket):
        pass
    def test_lambda_handler_downloads_json_files_to_intput_s3_bucket(self, mock_s3_bucket):
        pass
    def test_lambda_handler_downloads_parquet_files_to_input_s3_bucket(self, mock_s3_bucket):
        pass

class TestObfuscatorOutput:
    def test_lambda_handler_uploads_csv_files_to_output_s3_bucket(self, mock_s3_bucket):
        pass
    def test_lambda_handler_uploads_json_files_to_output_s3_bucket(self, mock_s3_bucket):
        pass
    def test_lambda_handler_uploads_parquet_files_to_output_s3_bucket(self, mock_s3_bucket):
        pass

class TestTranformationsIntoFileType:
    def test_lambda_handler_tranfroms_file_into_df(self, mock_s3_bucket):
        pass
        # response = tranform_file_into_df("address.pkl", mock_s3_bucket)
        # assert isinstance(response, pd.DataFrame)

    def test_lambda_handler_writes_output_file_into_bytestream(self, mock_s3_bucket):
        pass
        # response = tranform_file_into_df("address.pkl", mock_s3_bucket)
        # assert isinstance(response, pd.DataFrame)

class TestObfuscationOfCsvFiles:
    def test_lambda_handler_obfuscates_csv_files_correctly(self, mock_s3_bucket):
        pass
    def test_lambda_handler_obfuscates_json_files_correctly(self, mock_s3_bucket):
        pass
    def test_lambda_handler_obfuscates_parquet_files_correctly(self, mock_s3_bucket):
        pass

class TestObfuscatorReturnsStatusCode200ForInputFilesWithVariousSructures:
    def test_lambda_handler_returns_status_code_200_with_files_containing_various_number_of_columns(self, mock_s3_bucket):
        pass
    def test_lambda_handler_returns_status_code_200_with_files_containing_various_number_of_rows(self, mock_s3_bucket):
        pass
    def test_lambda_handler_returns_status_code_200_with_files_containing_various_number_of_columns_to_obfucate(self, mock_s3_bucket):
        pass
    def test_lambda_handler_uploads_returns_status_code_200_with_files_containing_various_number_of_columns(self, mock_s3_bucket):
        pass

class TestObfuscatorCatchesAndHandlesErrorsAndExceptions:
     def Test_Obfuscator_catches_and_handles_errors_and_exceptions(self, mock_s3_bucket):
         pass
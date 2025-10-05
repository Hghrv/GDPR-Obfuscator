from src import lambda_handler
from io import BytesIO
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

# Json event parameter for TestObfuscatorInput
json_event = {
    "file_to_obfuscate": "src/test_file.csv",
    "pii_fields": ["name", "email_address"]
}

# defining tests
class TestObfuscatorInput:
    def test_lambda_handler_downloads_csv_files_from_input_s3_bucket(self, mock_s3_bucket):
        pass
    def test_lambda_handler_downloads_json_files_from_input_s3_bucket(self, mock_s3_bucket):
        pass
    def test_lambda_handler_downloads_parquet_files_from_input_s3_bucket(self, mock_s3_bucket):
        pass

class TestObfuscatorOutput:
    def test_lambda_handler_uploads_csv_files_to_output_s3_bucket(self, mock_s3_bucket):
        pass
    def test_lambda_handler_uploads_json_files_to_output_s3_bucket(self, mock_s3_bucket):
        pass
    def test_lambda_handler_uploads_parquet_files_to_output_s3_bucket(self, mock_s3_bucket):
        pass

class TestTranformationsIntoFileType:
    # def test_lambda_handler_transforms_downloaded_file_into_df(self, mock_s3_bucket):
        # pass
        # response = load_into_dataframe("new_data/test_file.csv", mock_s3_bucket)
        # assert isinstance(response, pd.DataFrame)

    def test_lambda_handler_writes_output_file_into_bytestream(self, mock_s3_bucket):
        pass
        # response = load_into_dataframe("new_data/test_file.csv", context)
        # assert isinstance(response, csv.Bytestream)

class TestObfuscationOfCsvFiles:
    def test_lambda_handler_obfuscates_csv_files_correctly(self, mock_s3_bucket):
        pass
    def test_lambda_handler_obfuscates_json_files_correctly(self, mock_s3_bucket):
        pass
    def test_lambda_handler_obfuscates_parquet_files_correctly(self, mock_s3_bucket):
        pass

class TestObfuscatorReturnsStatusCode200ForInputFilesWithVariousStructures:
    def test_lambda_handler_returns_status_code_200_with_files_containing_various_number_of_columns(self, mock_s3_bucket):
        pass
    def test_lambda_handler_returns_status_code_200_with_files_containing_various_number_of_rows(self, mock_s3_bucket):
        pass
    def test_lambda_handler_returns_status_code_200_with_files_containing_various_number_of_columns_to_obfucate(self, mock_s3_bucket):
        pass
    def test_lambda_handler_uploads_returns_status_code_200_with_files_containing_various_number_of_columns(self, mock_s3_bucket):
        pass

class TestObfuscatorOutputHasExpectedObfuscatedContent:
    def test_obfuscator_output_has_expected_obfuscated_content_for_csv_file(self, mock_s3_bucket):
         pass
    def test_obfuscator_output_has_expected_obfuscated_content_for_json_file(self, mock_s3_bucket):
         pass
    def test_obfuscator_output_has_expected_obfuscated_content_for_pkl_file(self, mock_s3_bucket):
         pass

"""
class TestObfuscatorCatchesAndHandlesErrorsAndExceptions:
    
    LOGGER = logging.getLogger(__name__)
    
    def Test_Obfuscator_catches_and_logs_errors(self, caplog):
        expected_error_messsage = {
            "Error": {
                "Code": "NoSuchBucket",
                "Message": "The specified bucket does not exist",
            }
        }
        expected_error = botocore.exceptions.ClientError(
            expected_error_messsage, "ListObjectsV2"
        )

        with patch("boto3.client") as mock_boto_client:
            mock_s3 = mock_boto_client.return_value
            mock_s3.list_objects_v2.side_effect = expected_error

            with caplog.at_level(logging.ERROR):
                #get_data("not-a-bucket")

            assert "An error has occured with the client:" in caplog.text
            assert #get_data("not-a-bucket") == {"Error": str(expected_error)}
"""
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

# defining tests
class TestObfuscationOfCsvFiles:

    def test_lambda_handler_downloads_csv_files_from_input_s3_bucket(self):
        # Json event parameter for TestObfuscatorInput
        json_event = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name", "email_address"]
                    } 
        aws_context = 'provided_aws_context'
        
        # Tests parameters
        bucket_name = 'gdpr-data-storage'   # Input
        input_test_key = "new_data/test_file.csv"
        test_file = "src/test_file.csv"
        bucket_name_output = 'gdpr-obfuscator-ouput'    # Output 
        output_key = 'obfuscated_data/obfuscated-file.csv'
        
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=input_test_key, Body=test_file)

        response = lambda_handler(json_event, aws_context)
        assert response['statusCode'] == 200
        assert response['body'] == "Obfuscation completed successfully!"

    def test_lambda_handler_uploads_csv_files_to_output_s3_bucket(self):
        # Json event parameter for TestObfuscatorInput
        json_event = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name", "email_address"]
                    } 
        aws_context = 'provided_aws_context'
        
        # Tests parameters
        bucket_name = 'gdpr-data-storage'   # Input
        input_test_key = "new_data/test_file.csv"
        test_file = "src/test_file.csv"
        bucket_name_output = 'gdpr-obfuscator-ouput'    # Output 
        output_key = 'obfuscated_data/obfuscated-file.csv'
        
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=input_test_key, Body=test_file)
        
        lambda_handler(json_event, aws_context)
        response = s3_client.list_objects(Bucket=bucket_name_output, Prefix="obfuscated_data")
        objects = response.get('Contents')
        assert "src/output_test_file.csv" in objects[0]


    def test_lambda_handler_writes_output_csv_file_into_bytestream(self):
        # Json event parameter for TestObfuscatorInput
        json_event = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name", "email_address"]
                    } 
        aws_context = 'provided_aws_context'
        
        # Tests parameters
        bucket_name = 'gdpr-data-storage'   # Input
        input_test_key = "new_data/test_file.csv"
        test_file = "src/test_file.csv"
        bucket_name_output = 'gdpr-obfuscator-ouput'    # Output 
        output_key = 'obfuscated_data/obfuscated-file.csv'
        
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=input_test_key, Body=test_file)
        
        lambda_handler(json_event, aws_context)   # Calling the lambda function    
        response =s3_client.get_object(Bucket=bucket_name_output, Key=output_key)
            
        # Assert that stream_data is an instance of io.BytesIO
        assert isinstance(response, BytesIO), 'stream_data instance is not a a BytesIO object'

        # Assert that the content of stream_data is bytes-like
        response.seek(0)  # Reset the pointer to the start
        content = response.read()
        assert isinstance(content, (bytes, bytearray)), "Content of stream_data is not bytes-like"

    def test_lambda_handler_obfuscates_csv_files_correctly(self):
        # Json event parameter for TestObfuscatorInput
        json_event = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name", "email_address"]
                    } 
        aws_context = 'provided_aws_context'
        
        # Tests parameters
        bucket_name = 'gdpr-data-storage'   # Input
        input_test_key = "new_data/test_file.csv"
        test_file = "src/test_file.csv"
        bucket_name_output = 'gdpr-obfuscator-ouput'    # Output 
        output_key = 'obfuscated_data/obfuscated-file.csv'
        
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=input_test_key, Body=test_file)
        
        lambda_handler(json_event, aws_context)   # Calling the lambda function    
        response =s3_client.get_object(Bucket=bucket_name_output, Key=output_key)
        df = pd.read_csv(response)
        expected = pd.read_csv("src/output_test_file.csv")
        assert df == expected

    def test_lambda_handler_obfuscates_csv_files_correctly_with_different_event_scenarios(self):
        pass

class TestObfuscatorReturnsStatusCode200ForInputFilesWithVariousStructures:
    def test_lambda_handler_returns_status_code_200_with_files_containing_various_number_of_columns(self):
        json_event_1 = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name"]
                    } 
        aws_context = 'provided_aws_context'

        response = lambda_handler(json_event_1, aws_context)
        assert response['statusCode'] == 200
        assert response['body'] == "Obfuscation completed successfully!"
        
        json_event_2 = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name", "course", "email_adress"]
                    } 
        aws_context = 'provided_aws_context'

        response = lambda_handler(json_event_2, aws_context)
        assert response['statusCode'] == 200
        assert response['body'] == "Obfuscation completed successfully!"

################>>>> To add <<<<<#####################       
    def test_lambda_handler_returns_status_code_200_with_files_containing_various_number_of_rows(self):
        pass
    def test_lambda_handler_returns_status_code_200_with_files_containing_various_number_of_columns_to_obfucate(self):
        pass
    def test_lambda_handler_uploads_returns_status_code_200_with_files_containing_various_number_of_columns(self):
        pass
########################################################

class TestObfuscatorlogsErrors:  

    LOGGER = logging.getLogger(__name__)
    
    def Test_Obfuscatorlogs_errors(self, caplog):
        error_event = lambda_handler()
        assert "Error" in error_event

################>>>> To add <<<<<#####################
"""
class TestObfuscatorForJsonAndParquetFileTypes:
    
    def test_lambda_handler_obfuscates_json_files(self):
        pass
    def test_lambda_handler_obfuscates_parquet_files(self):
        pass

class TestObfuscatorOutputHasExpectedObfuscatedContent:
    def test_obfuscator_output_has_expected_obfuscated_content_for_csv_file(self):
         pass
    def test_obfuscator_output_has_expected_obfuscated_content_for_json_file(self):
         pass
    def test_obfuscator_output_has_expected_obfuscated_content_for_pkl_file(self):
         pass
"""
########################################################
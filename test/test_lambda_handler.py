from src.lambda_handler import lambda_handler
from io import BytesIO, StringIO 
import logging
import boto3
from moto import mock_aws
import pytest
import botocore.exceptions
from unittest.mock import patch
import pandas as pd
import json

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

        test_files = ["src/test_file.csv", "src/test_file.json", "src/test_file.pkl"]
        for file in test_files:
            s3.put_object(Bucket=bucket_name, Key=file)

        with open("./src/test_file.csv", "rb") as f:
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
        assert response['body'] == json.dumps("Obfuscation completed successfully!")

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
        assert "obfuscated_data/obfuscated-file.csv" in objects[0]['Key']


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
       
        # Assert that reponse is bytes-like
        assert isinstance(response['Body'].read(), (bytes, bytearray)), "Content of stream_data is not bytes-like"

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
        test_file = """student_id,name,course,cohort,graduation_date,email_address\n1234,'John Smith','Software','December','2024-03-31','j.smith@email.com'"""
        bucket_name_output = 'gdpr-obfuscator-ouput'    # Output 
        output_key = 'obfuscated_data/obfuscated-file.csv'
        
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=input_test_key, Body=test_file)
        
        lambda_handler(json_event, aws_context)   # Calling the lambda function    
        response =s3_client.get_object(Bucket=bucket_name_output, Key=output_key)
        csv_buffer = response["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(csv_buffer))
        expected_output = """student_id,name,course,cohort,graduation_date,email_address\n 1234,'***','Software','December','2024-03-31','***'"""
        expected = pd.read_csv(StringIO(expected_output))
        print(df)
        print(expected)
        print(df.loc[[0], ['name']])
        for column in ["student_id", "name", "course", "cohort", "graduation_date", "email_address"]:
            assert df.iloc[0][column]== expected.iloc[0][column]

    def test_lambda_handler_obfuscates_csv_files_correctly_with_different_event_scenarios(self):
        pass

class TestObfuscatorReturnsStatusCode200ForInputFilesWithVariousStructures:
    def test_lambda_handler_returns_status_code_200_with_various_number_of_fields_to_obfuscate(self):
        json_event_1 = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name"]
                    } 
        aws_context = 'provided_aws_context'

        response = lambda_handler(json_event_1, aws_context)
        assert response['statusCode'] == 200
        assert response['body'] == json.dumps("Obfuscation completed successfully!")
        
        json_event_2 = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name", "course", "email_adress"]
                    } 
        aws_context = 'provided_aws_context'

        response = lambda_handler(json_event_2, aws_context)
        assert response['statusCode'] == 200
        assert response['body'] == json.dumps("Obfuscation completed successfully!")

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

################>>>> To add after refactoring, debugging and successful tests <<<<<#####################
"""
class TestObfuscatorForJsonAndParquetFileTypes:
    
    def test_lambda_handler_handles_json_files_and_output_has_expected_obfuscated_json_content(self):
        json_event = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name", "email_address"]
                    } 
        aws_context = 'provided_aws_context'
        
        # Tests parameters
        bucket_name = 'gdpr-data-storage'   # Input
        input_test_key = "new_data/test_file.json"
        test_file = {
            "student_id": 1234,
            "name": 'John Smith',
            "course": 'Software',
            "cohort": 'December',
            "graduation_date": '2024-03-31',
            "email_address": 'j.smith@email.com'
        }
        bucket_name_output = 'gdpr-obfuscator-ouput'    # Output 
        output_key = 'obfuscated_data/obfuscated-file.json'
        
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=input_test_key, Body=test_file)
        
        lambda_handler(json_event, aws_context)   # Calling the lambda function    
        response =s3_client.get_object(Bucket=bucket_name_output, Key=output_key)
        buffer = response["Body"].read().decode("utf-8")
        data = json.loads(buffer)
        #df = pd.json_normalize(data)
        #print(json.dumps(data, indent=4))

        expected_output = {
            "student_id": 1234,
            "name": '***',
            "course": 'Software',
            "cohort": 'December',
            "graduation_date": '2024-03-31',
            "email_address": '***'
        }
        #expected = pd.read_csv(StringIO(expected_output))
        print(data)
        print(expected_output)
        assert json.dumps(data, indent=4) == expected_output

    def test_lambda_handler_handles_parquet_files_and_output_has_expected_obfuscated_parquet_content(self):
        json_event = {
                        "file_to_obfuscate": "new_data/test_file.csv", # input test-key
                        "pii_fields": ["name", "email_address"]
                    } 
        aws_context = 'provided_aws_context'
        
        # Tests parameters
        bucket_name = 'gdpr-data-storage'   # Input
        input_test_key = "new_data/test_file.parquet"
        test_file = {
                    "student_id": [1234],
                    "name": ['John Smith'],
                    "course": ['Software'],
                    "cohort": ['December'],
                    "graduation_date": ['2024-03-31'],
                    "email_address": ['j.smith@email.com']
                    }
        bucket_name_output = 'gdpr-obfuscator-ouput'    # Output 
        output_key = 'obfuscated_data/obfuscated-file.parquet'
        
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=input_test_key, Body=test_file)
        
        lambda_handler(json_event, aws_context)   # Calling the lambda function    
        response =s3_client.get_object(Bucket=bucket_name_output, Key=output_key)
        #csv_buffer = response["Body"].read().decode("utf-8")
        df = pd.read_parquet(output_key, storage_options={"anon": False})
        expected_output = {
                    "student_id": [1234],
                    "name": ['***'],
                    "course": ['Software'],
                    "cohort": ['December'],
                    "graduation_date": ['2024-03-31'],
                    "email_address": ['***']
                    }
        df_expected = pd.DataFrame(expected_output)
        print(df)
        print(df_expected)
        for column in ["student_id", "name", "course", "cohort", "graduation_date", "email_address"]:
            assert df.iloc[0][column] == df_expected.iloc[0][column]
"""

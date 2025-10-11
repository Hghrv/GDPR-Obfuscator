from src.utils.get_file_from_input_s3 import get_file_from_input_s3, load_into_dataframe
import logging
import csv
import pandas as pd
import boto3
from moto import mock_aws
import pytest
import botocore.exceptions
from testfixtures import LogCapture

# Setting s3 bucket fixture for mock tests with mock_aws
@pytest.fixture
def mock_s3_bucket():
    # Creating a mock-bucket
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-west-2")
        bucket_name = "test-bucket"
        s3.create_bucket(
            Bucket = bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        # Uploading test files to bucket
        test_files = ["src/test_file.csv", "src/test_file.json", "src/test_file.pkl"]
        for file in test_files:
            s3.put_object(Bucket=bucket_name, Key=file)

        # Uploading csv test content to bucket
        csv_content = "student_id,name,course,cohort,graduation_date,email_address\n1234,'John Smith','Software','December','2024-03-31','j.smith@email.com'"
        s3.put_object(Bucket=bucket_name, Key="new_data/test_file.csv", Body=csv_content)

        # Yielding the bucket name for testing
        yield bucket_name

# Defining class for ingestion test
class TestGetFileFromInputS3:

    def test_get_csv_file_from_input_s3(self, mock_s3_bucket):
        
        extracted = get_file_from_input_s3(mock_s3_bucket, "src/test_file.csv")
        assert isinstance(extracted, dict)
        assert all(var in extracted for var in ["Data_extracted", "body", "result"])            
        assert len(extracted) == 3
        assert extracted["result"] == "Success"

        response = extracted["Data_extracted"]
        assert isinstance(response, (bytes, bytearray)), "Response content is not bytes-like"

        read_response =  csv.reader(response)
        line_count_response = sum(1 for row in read_response)
        csv_reader = csv.reader("src/test_file.csv")
        line_count_expected = sum(1 for row in read_response)
        assert line_count_response == line_count_expected
        for row in range(line_count_expected):
            assert read_response[row] ==  csv_reader[row]

    LOGGER = logging.getLogger(__name__)
    
    def test_logs_when_file_is_extracted(self, caplog, mock_s3_bucket):
        
        with caplog.at_level(logging.INFO):
            get_file_from_input_s3(mock_s3_bucket, "src/test_file.csv")
        assert "File extracted from s3 bucket" in caplog.text

    def test_logs_error(self):
        
        with LogCapture() as log:
            error_event = get_file_from_input_s3("not-a-bucket", "src/test_file.csv")
        assert error_event["result"] == "Failure"
        assert "An error has occured with the client:" in str(log)        
        assert error_event["result"] == "Failure"

# Defining class for transformation into pandas dataframe
class TestLoadIntoDataframe:
    
    def test_load_into_dataframe(self, mock_s3_bucket):
        
        # Asserting that the installed version of pandas is 2.3.3, compatible with s3fs
        assert pd.__version__ == '2.3.3', f"Expected version '2.3.3', but got {pd.__version__}"
        print(pd.__version__)
        
        #with LogCapture() as log:
        #    response = load_into_dataframe(bucket_name, "src/test_file.csv")
        #assert "File content loaded into dataframe" in str(log)        
                
        # Define the bucket name and file key
        test_bucket_name = mock_s3_bucket
        test_file_key = "new_data/test_file.csv"
        
        load = load_into_dataframe(bucket_name=test_bucket_name, file_key=test_file_key)
        assert load["result"] == "Success"
        
        df = load["dataframe"]
        # Dataframe print for checks if needed
        print(df)

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert list(df.columns) == ["student_id", "name", "course", "cohort", "graduation_date", "email_address"]
        assert df.iloc[0]["student_id"] == 1234

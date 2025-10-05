from src.utils.get_file_from_input_s3 import get_file_from_input_s3, load_into_dataframe
import logging
import csv
import pandas as pd
import boto3
from moto import mock_aws
import pytest
import botocore.exceptions
from unittest.mock import patch

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
class TestGetFileFromInputS3:

    def test_get_csv_file_from_input_s3(self, mock_s3_bucket):
        
        extracted = get_file_from_input_s3(mock_s3_bucket, "new_data/test_file.csv")
        assert isinstance(extracted, dict)
        assert "Data_extracted" in extracted            
        assert len(extracted["Data_extracted"]) == 1
        assert "new_data/test_file.csv" in extracted["Data_extracted"]
            
        response = csv.reader(extracted["Data_extracted"])
        assert isinstance(response, csv.reader), "response is not a csv.reader instance"

    LOGGER = logging.getLogger(__name__)
    
    def test_logs_when_file_is_extracted(self, caplog, mock_s3_bucket):
        with caplog.at_level(logging.INFO):
            get_file_from_input_s3(mock_s3_bucket, "new_data/test_file.csv")
        assert "Extracting data from s3 bucket" in caplog.text

    def test_logs_error(self, caplog):
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
                get_file_from_input_s3("not-a-bucket")
            assert "An error has occured with the client:" in caplog.text
            assert get_file_from_input_s3("not-a-bucket") == {"Error": str(expected_error)}

class TestLoadIntoDataframe:
    
    def test_load_into_dataframe(self, mock_s3_bucket):
        extracted = get_file_from_input_s3(mock_s3_bucket, "new_data/test_file.csv")
        response = load_into_dataframe(extracted)
        assert isinstance(response, pd.DataFrame)

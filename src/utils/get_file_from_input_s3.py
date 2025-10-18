import pandas as pd
import boto3
import botocore.exceptions
import logging
from io import StringIO
import json


def get_file_from_input_s3(bucket_name, file_key):
    """
    Get data from s3 bucket
        Given an file location in s3 bucket,
        this funtion reads all the items and
        returns a dictionary with the file names
    - access the bucket
    - Retrieve data from bucket

    """
    # Initialising S3 client
    s3_client = boto3.client('s3')

    # Retrieving the CSV file from S3 bucket
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        response_body = response['Body']
        csv_data = response_body.read()
        print("Extracting data from s3 bucket")
        logging.info("File extracted from s3 bucket")
        return {
            "result": "Success",
            "body": response_body,
            "Data_extracted": csv_data
        }

    except botocore.exceptions.ClientError as e:
        logging.info("An error has occured with the client: %s", e)
        return {
            "result": "Failure",
            "Error": str(e)
        }


def load_csv_into_dataframe(bucket_name, file_key):

    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        buffer = response["Body"].read().decode("utf-8")
        df = {}
        # Load into Pandas DataFrame
        # for filename in os.listdir(file_key):
        if file_key.endswith(".csv"):
            df = pd.read_csv(StringIO(buffer))
            print("Loading file content into dataframe")
            logging.info("File content loaded into dataframe")

        elif file_key.endswith(".json"):
            data = json.loads(buffer)
            df = pd.json_normalize(data)

        elif file_key.endswith(".parquet"):
            df = pd.read_parquet(file_key, storage_options={"anon": False})

        else:
            return "No file (.csv or .json or .parquet) was found in input s3 bucket"

        print("Loading file content into dataframe")
        logging.info("File content loaded into dataframe")
        return {
            "result": "Success",
            "dataframe": df
        }

    except botocore.exceptions.ClientError as e:
        print("An error occured while loading file content into dataframe")
        logging.info("An error has occured with the client: %s", e)
        return {
            "result": "Failure",
            "Error": str(e)
        }

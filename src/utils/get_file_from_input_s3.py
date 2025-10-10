import pandas as pd
import boto3
import botocore.exceptions
import logging
from io import StringIO, BytesIO

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

def load_into_dataframe(bucket_name, file_key):
    """
    Load the downloaded file into a Pandas DataFrame
    and return the dataframe

    """
    try:
        #csv_buffer = BytesIO(file_content)
        #df = pd.read_csv(BytesIO(file_content))
        df = pd.read_csv('s3://{bucket_name}/{file_key}', delimiter=",", header=0)
        
        print("Loading file content into dataframe")
        logging.info("File content loaded into dataframe")
        return df
    
    except botocore.exceptions.ClientError as e:
        print("An error occured while loading file content into dataframe")
        logging.info("An error has occured with the client: %s", e)
        return {
                "result": "Failure",
                "Error": str(e)
                }
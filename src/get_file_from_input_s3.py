import pandas as pd
import boto3

def get_file_from_input_s3(bucket_name, file_key):
    """
    Get data from s3 bucket
        Given an file location in s3 bucket,
        this funtion reads all the items and
        returns a dictionary with the file names
    - access the bucket
    - get all data from bucket once

    """
    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Download the CSV file from S3 bucket
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    csv_data = response['Body'].read()

    return {"Files_extracted": csv_data}
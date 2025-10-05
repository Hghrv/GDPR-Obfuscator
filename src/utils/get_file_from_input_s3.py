import pandas as pd
import boto3
import botocore.exceptions
import logging

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
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csv_data = response['Body'].read()
        print("Extracting data from s3 bucket")
        return {"Data_extracted": csv_data}
    
    except botocore.exceptions.ClientError as e:
        logging.error("An error has occured with the client: %s", e)
        return {"Error": str(e)}

def load_into_dataframe(file_content):
    """
    Load the downloaded file into a Pandas DataFrame
    and return the dataframe

    """
    file_stream = BytesIO(file_content)
    df = pd.read_csv(file_stream)

    return df
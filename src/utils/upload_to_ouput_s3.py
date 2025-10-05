import pandas as pd
import boto3
import logging

def upload_to_ouput_s3(bucket_name_output, output_key, file_to_upload):
    """
    This function obfuscates values in specified columns with '*' characters
    - argument: the dataframe file and a list of personally identifiable fields to obfuscate
    - returns: the transformed dataframe
    """
    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name_output, Key=output_key, Body=file_to_upload)
        logging.info(f"writing to s3 ... {output_key}")
        print(f"Obfuscated file uploaded to s3://{bucket_name_output}/{output_key}")
        
        return {
                "obfuscated file": "{bucket_name_output}/{output_key}",
                "result": "Success"
                }
    
    except (ClientError, ParamValidationError) as e:
        logging.error(e)
        return {"result": "Failure"}

import csv
import json
import pyarrow.json as paj
import pyarrow.parquet as pap
import io
import pandas as pd
import boto3
from io import BytesIO, StringIO
from src.utils.get_file_from_input_s3 import get_file_from_input_s3, load_csv_into_dataframe
from src.utils.obfuscate import obfuscate
from src.utils.write_to_bytestream import write_to_bytestream
from src.utils.upload_to_ouput_s3 import upload_to_ouput_s3
from src.utils.csv_to_json import csv_to_json
from src.utils.json_to_parquet import json_to_parquet

def lambda_handler(event, context='aws_context'):
    """
    Arguments:
        Event: Json dictionary {
                                    'file_to_obfuscate': 's3:://path/to/file' 
                                    'pii_fields': [list of fields to obfuscate]
                                }
        Context: Provided AWS Lambda context 
                Context will be provided by AWS
                (ex: watchlogs, sns notifications if enabled, etc.)
                                                

    Returns:
        {
            'statusCode': 200,
            'body': json.dumps('Obfuscation completed successfully!')
        }
    """
    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Define bucket name and file keys
    bucket_name = 'gdpr-data-storage'   # Data Input
    bucket_name_output = 'gdpr-obfuscator-ouput'    # Data Output
    body = json.loads(event.get("body", "{}"))  # Parse the JSON string body  of the event
    file_key = body.get('file_to_obfuscate', 'new_data/test_file.csv')  # Access event keys
    columns_to_obfuscate = body.get('pii_fields', ["name", "email_address"])
    output_key = 'obfuscated_data/obfuscated-file.csv'  # Define output key
    output_key_json = 'obfuscated_data/obfuscated-file.json'
    output_key_parquet = 'obfuscated_data/obfuscated-file.parquet'

    try:        
        df_data = load_csv_into_dataframe(bucket_name, file_key)
        df = df_data['dataframe']
        
        # Obfuscate values in specified columns with '*' characters
        df_obfuscated = obfuscate(df, columns_to_obfuscate)
                
        # Write the modified DataFrame to a bytestream
        bytestream_output = write_to_bytestream(df_obfuscated)
        
        # Upload csv bytestream data of obfuscated file to output S3
        upload_to_ouput_s3(bucket_name_output, output_key, bytestream_output)
        
        
        # Upload json bytestream data of obfuscated file to output S3
        bytestream_output_json = csv_to_json(bytestream_output)
        upload_to_ouput_s3(bucket_name_output, output_key_json, bytestream_output_json)
        
        # Upload parquet bytestream data of obfuscated file to output S3
        bytestream_output_parquet = json_to_parquet(bytestream_output_json)    
        upload_to_ouput_s3(bucket_name_output, output_key_parquet, bytestream_output_parquet)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Obfuscation completed successfully!')
        }
    except Exception as e:
            print(e)

            raise e

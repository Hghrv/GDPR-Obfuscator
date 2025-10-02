import json
import pandas as pd
import boto3
from io import BytesIO
import copy

def lambda_handler(event, context):
    
    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Define bucket name and file key
    bucket_name = 'gdpr-data-storage'
    bucket_name_output = 'gdpr-obfuscator-ouput'
    file_key = copy.deepcopy(event.get('file_to_obfuscate', 'new_data/test_file.csv'))
    columns_to_obfuscate = copy.deepcopy(event.get('pii_fields', ["name", "email_address"]))
    output_key = 'obfuscated_data/obfuscated-file.csv'
   
    # Download the CSV file from S3
    response = s3_client.get_object(Bucket='gdpr-data-storage', Key='new_data/test_file.csv')
    csv_data = response['Body'].read()
    
    # Load the CSV into a Pandas DataFrame
    df = pd.read_csv(BytesIO(csv_data))

    # Obfuscate values in specified columns with '*' characters
    for column in columns_to_obfuscate:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: '*' * len(str(x)) if pd.notnull(x) else x)
    
    # Write the modified DataFrame to a bytestream
    output_buffer = BytesIO()
    df.to_csv(output_buffer, index=False)
    output_buffer.seek(0)

    # Upload bytestream data of obfuscated file to output S3
    s3_client.put_object(Bucket=bucket_name_output, Key=output_key, Body=output_buffer.getvalue())
    print(f"Obfuscated file uploaded to s3://{bucket_name}/{output_key}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Obfuscation completed successfully!')
    }

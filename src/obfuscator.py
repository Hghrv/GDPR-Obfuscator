import json
import pandas as pd
import boto3
from io import BytesIO

def lambda_handler(event, context):
    
    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Define bucket name and file keys
    bucket_name = 'gdpr-data-storage'   # Data Input
    bucket_name_output = 'gdpr-obfuscator-ouput'    # Data Output
    body = json.loads(event.get("body", "{}"))  # Parse the JSON string body  of the event
    file_key = body.get('file_to_obfuscate', 'new_data/test_file.csv')  # Access event keys
    columns_to_obfuscate = body.get('pii_fields', ["name", "email_address"])
    output_key = 'obfuscated_data/obfuscated-file.csv'  # Define output key
   
    # Download the CSV file from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
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
    print(f"Obfuscated file uploaded to s3://{bucket_name_output}/{output_key}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Obfuscation completed successfully!')
    }

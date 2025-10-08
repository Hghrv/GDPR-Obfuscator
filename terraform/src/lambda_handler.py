import json
import pandas as pd
import boto3
from io import BytesIO
from src.utils.get_file_from_input_s3 import get_file_from_input_s3, load_into_dataframe
from src.utils.obfuscate import obfuscate
from src.utils.write_to_bytestream import write_to_bytestream
from src.utils.upload_to_ouput_s3 import upload_to_ouput_s3

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

    try:
        # Download the CSV file from S3
        file = get_file_from_input_s3(bucket_name, file_key)
        # response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        # csv_data = response['Body'].read()
        
        # Load the CSV into a Pandas DataFrame
        df_data = load_into_dataframe(file)
        # df = pd.read_csv(BytesIO(csv_data))

        # Obfuscate values in specified columns with '*' characters
        df_obfuscated = obfuscate(df_data)
        # for column in columns_to_obfuscate:
        #    if column in df.columns:
        #        df[column] = df[column].apply(lambda x: '*' * len(str(x)) if pd.notnull(x) else x)
        
        # Write the modified DataFrame to a bytestream
        bytestream_output = write_to_bytestream(df_obfuscated)
        # output_buffer = BytesIO()
        # df.to_csv(output_buffer, index=False)
        # output_buffer.seek(0)

        # Upload bytestream data of obfuscated file to output S3
        upload_to_ouput_s3(bucket_name_output, output_key, bytestream_output)
        # s3_client.put_object(Bucket=bucket_name_output, Key=output_key, Body=output_buffer.getvalue())
        # print(f"Obfuscated file uploaded to s3://{bucket_name_output}/{output_key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Obfuscation completed successfully!')
        }
    except Exception as e:
            print(e)

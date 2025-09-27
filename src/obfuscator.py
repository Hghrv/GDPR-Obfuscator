import copy
import pandas as pd
import boto3
from io import StringIO

# Initialize S3 client
s3 = boto3.client('s3')

# Defining the obfuscating module
def obfuscate(file_to_obfuscate: str="", pii_fields: list= []):
    pass

    # Define bucket name and file key
    bucket_name = 'gdpr_data-storage'
    file_key = copy.deepcopy(file_to_obfuscate)
    columns_to_obfuscate = copy.deepcopy(pii_fields)
    output_key = 'obfuscated_data/obfuscated-file.csv'
    output_key_1 = 'obfuscated_data/obfuscated-bytestream.txt'

# def obfuscate_csv(bucket_name, file_key, columns_to_obfuscate, output_key):
    # Download the CSV file from S3
    csv_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    csv_data = csv_obj['Body'].read().decode('utf-8')
    
    # Load the CSV into a Pandas DataFrame
    df = pd.read_csv(StringIO(csv_data))
    
    # Obfuscate values in specified columns with '*' characters
    for column in columns_to_obfuscate:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: '*' * len(str(x)) if pd.notnull(x) else x)
    
    # Save the modified DataFrame back to a CSV
    csv_buffer = StringIO()
    
    df.to_csv(csv_buffer, index=False)
    
    # Convert the CSV to bytestream representation
    bytestream_file = csv_buffer.encode('utf-8')
    
    # Upload the obfuscated CSV back to S3
    s3.put_object(Bucket=bucket_name, Key=output_key, Body=csv_buffer.getvalue())
    print(f"Obfuscated file uploaded to s3://{bucket_name}/{output_key}")

    # Upload the bytstream representation back to S3
    s3.put_object(Bucket=bucket_name, Key=output_key, Body=bytestream_file.getvalue())
    print(f"Bytestream representation uploaded to s3://{bucket_name}/{output_key_1}")


"""
# Example usage
bucket_name = 'your-s3-bucket-name'
file_key = 'input-folder/input-file.csv'
output_key = 'output-folder/obfuscated-file.csv'
columns_to_obfuscate = ['column1', 'column2']  # Replace with your column names

obfuscate_csv(bucket_name, file_key, columns_to_obfuscate, output_key)
"""










"""1

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import boto3
import pandas as pd
from io import StringIO
import csv

def obfuscate(file_to_obfuscate: str="", pii_fields: list= []):
    pass
    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Define bucket name and file key
    bucket_name = 'gdpr_data-storage'
    file_key = file_to_obfuscate

    # Fetch the file from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)

    # Read the file content and asigh it to a variable csv_content
    csv_content = response['Body'].read().decode('utf-8')

    # Load the CSV content into a Pandas DataFrame
    df = pd.read_csv(StringIO(csv_content))

    # Display the DataFrame
    print(df)

    # Display the pii_fields
    print(pii_fields)
    
    # Get list of columns:
    columns_list = df.columns.tolist()
    print(columns_list) 
    
    # We are assuming that the provided input list as been effectuvely tested to be belong the list of columns prior to integration
    # Define the output file 
    output_file = 's3://gdpr_data-storage/obfuscated_data/obfuscated-file.csv'

    # 



















    # Access and obfucate the sensitive strings in the CSV content
    for column_name in list:
        # Access string intersecting row of index 1 and column_name
        string_to_obfuscate = df.loc[1, column_name]
        print(string_to_obfuscate)
"""

"""2

        # Function to pad the string to be a multiple of 16 bytes
        def pad(data):
            return data + (16 - len(data) % 16) * chr(16 - len(data) % 16)

        # Function to unpad the string after decryption
        def unpad(data):
            return data[:-ord(data[-1])]

        # Encrypt a string
        def encrypt_string(key, plaintext):
            cipher = AES.new(key, AES.MODE_CBC)  # Using CBC mode
            iv = cipher.iv  # Initialization vector
            padded_data = pad(plaintext).encode('utf-8')
            encrypted_data = cipher.encrypt(padded_data)
            # Combine IV and encrypted data, then encode in Base64 for readability
            return base64.b64encode(iv + encrypted_data).decode('utf-8')

        # Decrypt a string
        def decrypt_string(key, encrypted_text):
            encrypted_data = base64.b64decode(encrypted_text)
            iv = encrypted_data[:16]  # Extract the IV
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = cipher.decrypt(encrypted_data[16:])
            return unpad(decrypted_data.decode('utf-8'))

        # Example usage
        if __name__ == "__main__":
            
            # Generate a random 16-byte key (AES-128)
            key = get_random_bytes(16)
            
            # String to obfuscate
            original_string = "Hello, PyCryptodome!" # string_data arg
            print("Original String:", original_string)
            
            # Encrypt the string
            encrypted = encrypt_string(key, original_string)
            print("Encrypted String:", encrypted)
            
            # Decrypt the string
            decrypted = decrypt_string(key, encrypted)
            print("Decrypted String:", decrypted)
        """

  
from io import BytesIO, StringIO
import csv
import json
import logging

def csv_to_json(csv_bytes):
    """
    This function transforms csv bytestream data into a json bytestream data
    - argument: the csv bytestream data
    - returns : a json bytestream file with .json extension
    """
        # Input CSV bytestream
        #csv_bytes = BytesIO(b"Name,Age,City\nAlice,30,London\nBob,25,Paris")
        
    try:
        bytestream_output_json = {}
        # Loading csv bytestream
        csv_file = StringIO(csv_bytes.decode('utf-8'))
        reader = csv.DictReader(csv_file)

        # Converting csv rows to json
        bytestream_output_json = json.dumps([row for row in reader])

        # Returning json bytestream
        return bytestream_output_json.encode('utf-8')
    
    except Exception as e:
        print(e)
        raise e   

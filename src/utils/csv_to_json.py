from io import BytesIO, StringIO
import csv
import json

def csv_to_json(csv_bytes):
    """
    This function transforms csv bytestream data into a json bytestream data
    - argument: the csv bytestream data
    - returns : a json bytestream file with .json extension
    """
    # Input CSV bytestream
    #csv_bytes = BytesIO(b"Name,Age,City\nAlice,30,London\nBob,25,Paris")
    
    bytestream_output_json = {}
    # Convert CSV bytes to JSON bytes
    csv_file = StringIO(csv_bytes.getvalue().decode('utf-8'))
    reader = csv.DictReader(csv_file)

    # Convert rows to JSON
    json_data = json.dumps([row for row in reader])

    # Output JSON bytestream
    json_bytes = BytesIO(json_data.encode('utf-8'))
       

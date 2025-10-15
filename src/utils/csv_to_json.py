
# Upload json bytestream data of obfuscated file to output S3
def csv_to_json(csv_bytes):
    """
    This function uploads json bytestream data of obfuscated file to output S3
    - argument: the dataframe file and a corresponding list of personally 
                identifiable fields to obfuscate
    - returns : a json bytestream file with .jon
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
       

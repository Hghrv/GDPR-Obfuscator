from io import BytesIO, StringIO
import pyarrow.json as paj
import pyarrow.parquet as pap

bytestream_output_parquet = {}
def json_to_parquet(json_bytes):
    """
    This function transforms json bytestream data into a parquet bytestream data
    - argument: the json bytestream data 
    - returns : a parquet bytestream file with .parquet extension
    """
    # Convert JSON bytestream to a PyArrow Table
    json_stream = BytesIO(json_bytes)
    table = paj.read_json(json_stream)
            
    # Convert the PyArrow Table to a Parquet bytestream
    parquet_stream = BytesIO()
    pap.write_table(table, parquet_stream)
            
    # Return the Parquet bytestream
    return parquet_stream.getvalue()

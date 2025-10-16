from io import BytesIO
import pyarrow as pa
import pyarrow.parquet as pap
import pandas as pd
import json

bytestream_output_parquet = {}
def json_to_parquet(json_bytes: bytes) -> bytes:
    """
    This function transforms json bytestream data into a parquet bytestream data
    - argument: the json bytestream data 
    - returns : a parquet bytestream file with .parquet extension
    """
    try:
        
        # Laoding the json bytestream
        json_data = [json.loads(line) for line in BytesIO(json_bytes).readlines()]
        
        # Converting json bytestream data to a Pandas DataFrame
        df = pd.DataFrame(json_data)
        
        # Converting DataFrame to Parquet bytestream
        parquet_buffer = BytesIO()
        table = pa.Table.from_pandas(df)   # Converting json bytestream to a PyArrow Table
        pap.write_table(table, parquet_buffer)  # Converting the PyArrow Table to a Parquet bytestream
        
        return parquet_buffer.getvalue()
    
        """# Convert JSON bytestream to a PyArrow Table
        json_stream = BytesIO(json_bytes)
        table = paj.read_json(json_stream)
                
        # Convert the PyArrow Table to a Parquet bytestream
        parquet_stream = BytesIO()
        pap.write_table(table, parquet_stream)
                
        # Return the Parquet bytestream
        return parquet_stream.getvalue()"""
    
    except Exception as e:
        print(e)
        raise e 

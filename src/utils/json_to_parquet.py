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
        json_data = [json.loads(line)
                    for line in BytesIO(json_bytes).readlines()]

        # Converting json bytestream data to a Pandas DataFrame
        df = pd.DataFrame(json_data)

        # Converting DataFrame to Parquet bytestream
        parquet_buffer = BytesIO()
        # Converting json bytestream to a PyArrow Table
        table = pa.Table.from_pandas(df)
        # Converting the PyArrow Table to a Parquet bytestream
        pap.write_table(table, parquet_buffer)

        return parquet_buffer.getvalue()

    except Exception as e:
        print(e)
        raise e

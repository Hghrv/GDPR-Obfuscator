import pandas as pd
import logging
from io import BytesIO


def write_to_bytestream(df):
    """
    This function obfuscates values in specified columns with '*' characters
    - argument: the dataframe file and a list of personally identifiable fields to obfuscate
    - returns: the transformed dataframe
    """
    try:
        output_buffer = BytesIO()
        df.to_csv(output_buffer, index=False)
        output_buffer.seek(0)
        bytestream = output_buffer.getvalue()
        print("Writing bytestream representation")
        logging.info("Bytestream representation successful")
        return bytestream

    except (Exception) as e:
        logging.error(e)
        print(e)
        return {"result": "Failure"}

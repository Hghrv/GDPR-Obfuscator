import pandas as pd
from io import BytesIO

def load_into_dataframe(file_content):
    """
    Load the downloaded file into a Pandas DataFrame
    and return the dataframe

    """
    df = pd.read_csv(BytesIO(file_content))

    return df
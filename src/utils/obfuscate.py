import pandas as pd
import logging


def obfuscate(df, columns_to_obfuscate):
    """
    This function obfuscates values in specified columns with '***' characters
    - argument: the dataframe file and a corresponding list of personally 
                identifiable fields to obfuscate
    - returns : the transformed dataframe
    """
    try:
        for column in columns_to_obfuscate:
            if column in df.columns:
                df[column] = df[column].apply(
                    lambda x: "'***'" if pd.notnull(x) else x)
        print("Obfuscating specified fields")

        logger = logging.getLogger(__name__)
        logger.info("Success: Specified fields obfuscated")

        return df

    except Exception as e:
        print(e)
        raise e

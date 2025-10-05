import pandas as pd

def obfuscate(df, columns_to_obfuscate):
    """
    This function obfuscates values in specified columns with '*' characters
    - argument: the dataframe file and a list of personally identifiable fields to obfuscate
    - returns: the transformed dataframe
    """
    for column in columns_to_obfuscate:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: '*' * len(str(x)) if pd.notnull(x) else x)
    print("Obfuscating specified fields")
    
    return df

from src.utils.json_to_parquet import json_to_parquet
import pyarrow.parquet as pap
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from io import BytesIO

class TestJsonToParquet:
    def test_transformation_returns_with_correct_parquet_format(self):

        test_json_bytes = b'{"student_id": 1234, "name": "***", "course": "Software", "cohort": "December", "graduation_date": "2024-03-31", "email_address": "***"}'
        response = json_to_parquet(test_json_bytes)
        assert isinstance(response, (bytes, bytearray)), "Output is not byte-like"

        # Read Parquet bytestream back into a DataFrame
        parquet_buffer = BytesIO(response)
        table = pap.read_table(parquet_buffer)
        df = table.to_pandas()
        
        # Expected DataFrame
        expected_df = pd.DataFrame([{
                                    "student_id": 1234,
                                    "name": '***',
                                    "course": 'Software',
                                    "cohort": 'December',
                                    "graduation_date": '2024-03-31',
                                    "email_address": '***'
                                    }])
        
        # Assert DataFrame equality
        pd.testing.assert_frame_equal(df, expected_df)
        
        """ 
            expected_parquet_bytes = ( b'[{"student_id": "[1234]", '
                                b'"name": "[\'***\']", '
                                b'"course": "[\'Software\']", '
                                b'"cohort": "[\'December\']", '
                                b'"graduation_date": "[\'2024-03-31\']", '
                                b'"email_address": "[\'***\']"}]')
            
        assert response == expected_parquet_bytes
        assert isinstance(response, (bytes, bytearray)), "Output is not byte-like"
        """


    def test_logs_errors(self, caplog):
        with pytest.raises(Exception):
            error_event = json_to_parquet('non-valid-argument')
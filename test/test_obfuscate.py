from src.utils.obfuscate import obfuscate
import logging
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pprint import pprint

class TestObfuscate:
    def test_obfuscation_occurs_in_correct_fields_as_expected(self):

        df = pd.read_csv('src/test_file.csv')
        pii_list = ["name", "email_address"]
        expected = {            
            "student_id": [1234],
            "name": ["'***'"],
            "course": ["'Software'"],
            "cohort": ["'December'"],
            "graduation_date": ["'2024-03-31'"],
            "email_address": ["'***'"]
        }
        df_expected = pd.DataFrame(expected)
        response = obfuscate(df, pii_list)
        pprint(df_expected)
        pprint(df_expected["course"])
        pprint(response)
        pprint(response["course"])
        assert_frame_equal(response, df_expected)

    LOGGER = logging.getLogger(__name__)
    
    def test_logs_when_dataframe_is_obfuscated(self, caplog):
        
        df =pd.read_csv('src/test_file.csv')
        pii_list = ["name", "email_address"]
        
        with caplog.at_level(logging.INFO):
           obfuscate(df, pii_list)
        assert "Success: Specified fields obfuscated" in caplog.text

    def test_logs_error(self, caplog):
        with pytest.raises(Exception):
            error_event = obfuscate(1, 2)
    

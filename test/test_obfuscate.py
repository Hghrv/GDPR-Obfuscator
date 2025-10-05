from src.utils import obfuscate
import logging
import pandas as pd

class TestObfuscate:
    def test_obfuscate_(self):

        df = pd.read_csv('src/test_file.csv')
        pii_list = ["name", "email_address"]
        expected = {            
            "student_id": 1234,
            "name": "************",
            "course": "Software",
            "graduation_date": "2024-03-31",
            "email_address": "*****************"
        }

        response = obfuscate(df, pii_list)
        assert response == expected

    LOGGER = logging.getLogger(__name__)
    
    def test_logs_when_dataframe_is_obfuscated(self, caplog):
        
        df =pd.read_csv('src/test_file.csv')
        pii_list = ["name", "email_address"]
        with caplog.at_level(logging.INFO):
           obfuscate(df, pii_list)
        assert "Obfuscating specified fields" in caplog.text

    def test_logs_error(self, caplog):
        
        error_event = obfuscate()
        assert "Error" in error_event

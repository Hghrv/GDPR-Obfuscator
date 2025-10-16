from src.utils.csv_to_json import csv_to_json
import logging
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pprint import pprint

from io import BytesIO, StringIO
import csv
import json

class TestCsvToJson:
    def test_transformation_returns_with_correct_json_dictionary(self):
        test_csv_bytes = b"student_id,name,course,cohort,graduation_date,email_address\n1234,'***','Software','December','2024-03-31','***'"
        response = csv_to_json(test_csv_bytes)
        expected_json_bytes = ( b'[{"student_id": "1234", '
                                b'"name": "\'***\'", '
                                b'"course": "\'Software\'", '
                                b'"cohort": "\'December\'", '
                                b'"graduation_date": "\'2024-03-31\'", '
                                b'"email_address": "\'***\'"}]')
        
        assert response == expected_json_bytes
        assert isinstance(response, (bytes, bytearray)), "Output is not byte-like"

    def test_logs_errors(self, caplog):
        with pytest.raises(Exception):
            error_event = csv_to_json('non-valid-argument')

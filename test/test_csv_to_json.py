from src.utils.json_to_parquet import json_to_parquet
import logging
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pprint import pprint

class TestObfuscate:
    def test_obfuscation_occurs_in_correct_fields_as_expected(self):
        pass
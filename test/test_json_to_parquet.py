from src.utils.obfuscate import obfuscate
import logging
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pprint import pprint

class TestJsonToParquet:
    def test_obfuscation_occurs_in_correct_fields_as_expected(self):
        pass
from src.utils.write_to_bytestream import write_to_bytestream
import logging
import pandas as pd
from io import BytesIO
from testfixtures import LogCapture

class TestWriteToBytestream:
    def test_write_to_bytestream(self):
        
        df = pd.read_csv('src/test_file.csv')
        stream_data = write_to_bytestream(df)
        assert isinstance(stream_data, (bytes, bytearray)), "Content of stream_data is not bytes-like"
    
    LOGGER = logging.getLogger(__name__)
    
    def test_logs_when_obfuscated_file_is_written_to_bytestream(self):
        
        df = pd.read_csv('src/test_file.csv')
        
        with LogCapture() as log:
            write_to_bytestream(df)
        assert "Bytestream representation successful" in str(log)

    def test_logs_error(self):
                
        with LogCapture() as log:
            error_event = write_to_bytestream('invalid_input')
            assert error_event["result"] == "Failure"
            assert "root ERROR\n  'str' object has no attribute 'to_csv'" in str(log)

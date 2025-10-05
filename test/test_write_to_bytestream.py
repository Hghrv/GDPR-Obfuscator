from src.utils import write_to_bytestream
import logging
import pandas as pd
from io import BytesIO

class TestWriteToBytestream:
    def test_write_to_bytestream(self, mock_s3_bucket):
        
        df = pd.read_csv('src/test_file.csv')
        stream_data = write_to_bytestream(df)

        # Assert that stream_data is an instance of io.BytesIO
        assert isinstance(stream_data, BytesIO), 'stream_data instance is not a a BytesIO object'

        # Assert that the content of stream_data is bytes-like
        stream_data.seek(0)  # Reset the pointer to the start
        content = stream_data.read()
        assert isinstance(content, (bytes, bytearray)), "Content of stream_data is not bytes-like"
        LOGGER = logging.getLogger(__name__)
    
    def test_logs_when_obfuscated_file_is_written_to_bytestream(self, caplog):
        
        df = pd.read_csv('src/test_file.csv')
        stream_data = write_to_bytestream(df)
        with caplog.at_level(logging.INFO):
            write_to_bytestream(df)
        assert "Writing bytestream representation" in caplog.text

    def test_logs_error(self, caplog):
        
        error_event = write_to_bytestream()
        assert "Error" in error_event
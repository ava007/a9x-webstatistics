import unittest
from pathlib import Path

from a9x_webstatistics.main import *
from a9x_webstatistics.updatestatistics import *

class TestMain010(unittest.TestCase):

    def test_main010(self):
        # calling runws expecting return 0
        assert runws() == 0
        file = Path("webstat.json")  
        with open(file) as f:  
            file_data = f.read()  
        print(str(file_data))
        contents = json.loads(file_data)
        assert '20240130144922' in contents['timelastrec']

if __name__ == '__main__':
    unittest.main()

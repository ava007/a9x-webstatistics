import unittest
import sys
from pathlib import Path

from a9x_webstatistics.main import *
from a9x_webstatistics.updatestatistics import *

class TestMain010(unittest.TestCase):

    def test_main010(self):
        # calling runws expecting return 0
        print("sys.argv: " + str(sys.argv))
        sys.argv[1:] = ["infile","test_access_monthly02.log"]
        print("sys.argv 2: " + str(sys.argv))
        assert runws(["infile","test_access_monthloy02.log"]) == 0
        file = Path("webstat.json")  
        with open(file) as f:  
            file_data = f.read()  
        print(str(file_data))
        contents = json.loads(file_data)
        assert '20240130144922' in contents['timelastrec']

if __name__ == '__main__':

    print("sys.argv: " + str(sys.argv))
    sys.argv[4:] = ["-infile","/test_access_monthly02.log"]
    print("sys.argv 2: " + str(sys.argv))
    unittest.main()

import unittest
import sys
from pathlib import Path

from a9x_webstatistics.gencockpit import *

class TestGencockpit010(unittest.TestCase):

    def test_gencockpit010(self):
        # calling runws expecting return 0
        assert runws(infile="webstat.json") == 0
        #file = Path("webstat.json")  
        #with open(file) as f:  
        #    file_data = f.read()  
        #print(str(file_data))
        #contents = json.loads(file_data)
        #assert '20240227151514' in contents['timelastrec']

if __name__ == '__main__':
    unittest.main()

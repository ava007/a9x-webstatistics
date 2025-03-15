import unittest
import sys
from pathlib import Path

from a9x_webstatistics.main import *
from a9x_webstatistics.updatestatistics import *

class TestMain030(unittest.TestCase):

    def test_main030(self):
        # calling runws expecting return 0
        assert runws(statfile="webstat.json", infile="nginx_access3.log", geoip="GeoIP2-Country.mmdb", verbosity="0", domain="http://logikfabrik.com") == 0
        file = Path("webstat.json")  
        with open(file) as f:  
            file_data = f.read()  
        print(str(file_data))
        contents = json.loads(file_data)
        print(str(contents))
        assert '20250315175938' in contents['timelastrec']
      

if __name__ == '__main__':
    unittest.main()

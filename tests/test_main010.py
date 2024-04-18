import unittest
from pathlib import Path

from a9x_webstatistics.main import *

class TestMain010(unittest.TestCase):

    def test_main010(self):
        print("home: " + str(Path.home()) )
        p = Path('.')
        [x for x in p.iterdir() if x.is_dir()]
        # calling runws expecting return 0
        #assert runws() == 0
        #file = Path("webstat.json")  
        #with open(file) as f:  
        #    file_data = f.read()  
        #print(str(file_data))
        #contents = json.loads(file_data)
        #assert '19991231235959' in contents['timelastrec']

if __name__ == '__main__':
    unittest.main()

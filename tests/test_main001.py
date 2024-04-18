import unittest
from pathlib import Path

from a9x_webstatistics import main

class TestMain(unittest.TestCase):

    def test_main(self):
        print("home: " + str(Path.home()) )
        # calling runws expecting return 0
        assert runws() == 0
        file = Path("webstat.json")  
        with open(file) as f:  
            input_data = f.read()  
        assert timelastrec(input_data) == '19991231235959'

if __name__ == '__main__':
    unittest.main()

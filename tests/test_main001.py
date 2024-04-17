import unittest
import pathlib

import a9x_webstatistics.main


class TestMain(unittest.TestCase):

    def test_main(self):
        file = pathlib.Path("webstat.json")  
        with open(file) as f:  
            input_data = f.read()  
        #expected = "Jerry was born in 1968"  
        assert timelastrec(input_data) == '19991231235959'
        #self.assertEqual((Number(7) + Number(6)).value, 13)

if __name__ == '__main__':
    unittest.main()

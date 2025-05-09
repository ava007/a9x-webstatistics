import unittest
from pathlib import Path

from a9x_webstatistics.main import *
from a9x_webstatistics.updatestatistics import upd
from a9x_webstatistics.migV0001.migrateV0001sub0001 import *
from subprocess import run

class TestMain(unittest.TestCase):

    def test_main(self):
        print("home: " + str(Path.home()) )
        #cmddata = run('find / -name "Geo*" -print', capture_output=True, shell=True, text=True)
        #print(cmddata.stdout) 
        #print(cmddata.stderr) 

        # calling runws expecting return 0
        assert runws(statfile="webstat.json", infile="nginx_access2022_00.log", geoip="GeoIP2-Country.mmdb", verbosity="0", domain="http://logikfabrik.com") == 0
        file = Path("webstat.json")  
        with open(file) as f:  
            file_data = f.read()  
        print(str(file_data))
        contents = json.loads(file_data)

        # check with nginx_access0.log
        assert '20220923165725' in contents['timelastrec']

       # calling runws expecting return 0
        assert runws(statfile="webstat.json", infile="nginx_access2022_01.log", geoip="GeoIP2-Country.mmdb", verbosity="0", domain="http://logikfabrik.com") == 0
        file = Path("webstat.json")  
        with open(file) as f:  
            file_data = f.read()  
        print(str(file_data))
        contents = json.loads(file_data)

        # check with nginx_access0.log  [21/Dec/2022:15:19:03]
        assert '20221221151903' in contents['timelastrec']


if __name__ == '__main__':
    unittest.main()

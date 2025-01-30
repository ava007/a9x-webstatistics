import unittest
import sys
from pathlib import Path
from subprocess import run

#from a9x_webstatistics.gencockpitV0001 import *
from a9x_webstatistics.gencockpitsubV0001 import cockpitlanguages
from a9x_webstatistics.gencockpitV0001 import runGenCockpitV0001

class TestGencockpit010(unittest.TestCase):

    def test_gencockpit010(self):
        cmddata = run('ls -altr', capture_output=True, shell=True, text=True)
        print(cmddata.stdout) 
        
        # calling runws expecting return 0
        assert runGenCockpitV0001(infile="webstat.json",outfile="webstat.html",domain="https://logikfabrik.com", omit='', efeature='') == 0
        with open('webstat.html') as f:  
            file_data = f.read()  
        print(str(file_data))
        

if __name__ == '__main__':
    unittest.main()

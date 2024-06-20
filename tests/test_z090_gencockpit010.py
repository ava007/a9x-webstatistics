import unittest
import sys
from pathlib import Path
from subprocess import run

from a9x_webstatistics.gencockpit import *

class TestGencockpit010(unittest.TestCase):

    def test_gencockpit010(self):
        cmddata = run('ls -altr', capture_output=True, shell=True, text=True)
        print(cmddata.stdout) 
        
        # calling runws expecting return 0
        assert runGenCockpit(infile="webstat.json",outfile="webstat.html",domain="https://logikfabrik.com") == 0
        with open('webstat.html') as f:  
            file_data = f.read()  
        print(str(file_data))
        

if __name__ == '__main__':
    unittest.main()

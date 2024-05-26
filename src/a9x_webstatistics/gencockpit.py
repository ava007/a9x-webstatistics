# -*- coding: utf-8 -*-
import io, sys, argparse, json, ast
from copy import deepcopy
from datetime import datetime

def genHeader():
    h = '<html>' + "\n"
    h += '<body>' + "\n"
    h += '<div> <canvas id="myChart"></canvas> </div>' + "\n"
    h += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>' + "\n"
    h += '<script>' + "\n" + 'const ctx = document.getElementById(\'myChart\');' + "\n"
    return h
def runGenCockpit(infile, outfile):
    with open(infile) as json_file:
        d = json.load(json_file) 

        lbl = []
        dta = []

        for e in d['days']:
            lbl.append(e)
            dta.append(d['days'][e]['device_hits']['desktop'])

        h = genHeader()
        h += 'new Chart(ctx, {'  + "\n"
        h += ' type: \'bar\','   + "\n"
        h += '  data: { ' + "\n" +  '  labels: ' + str(lbl) + ',' + "\n"
        h += ' datasets: [{ label: \'User Visits\',  data: ' + str(dta) + ','
        h += '}]' + "\n"
        h += ' },' + "\n" + '});' + "\n"
        h += '</script></body></html>'

        # write html to file:
        outfile = open(outfile, "w")
        outfile.write(h)
        outfile.close()

        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False,
        prog='a9x_webstatistics',
        epilog="Version: "+ version('a9x-webstatistics')
    )
    parser.add_argument("-i", "--infile", help="json file that contains calculated statistics", default="webstat.json")
    parser.add_argument("-o", "--outfile", help="html file that contains html cockpit", default="webstat.html")
    args, unknown = parser.parse_known_args()

    runGenCockpit(infile=args.infile, outfile=args.outfile)

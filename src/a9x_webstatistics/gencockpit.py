# -*- coding: utf-8 -*-
import io, sys, argparse, json, ast
from copy import deepcopy
from importlib.metadata import version
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
        dta_mobile = []

        try:
            for e in d['days']:
                lbl.append(e)
                if 'desktop' in d['days'][e]['device_hits']:
                    dta.append(d['days'][e]['device_hits']['desktop'])
                else:
                    dta.append(0)
                if 'mobile' in d['days'][e]['device_hits']:
                    dta_mobile.append(d['days'][e]['device_hits']['mobile'])
                else:
                    dta_mobile.append(0)

        except KeyError:
            print('KeyError occured!' + str(d['days'][e]) )
            raise
              
        h = genHeader()
        h += 'new Chart(ctx, {'  + "\n"
        h += ' type: \'bar\','   + "\n"
        h += ' responsive: true,' + "\n"
        h += ' options: { scales: {x:{ stacked: true}, y:{ stacked: true }}},' + "\n"
        h += ' data: { ' + "\n" +  '  labels: ' + str(lbl) + ',' + "\n"
        h += ' datasets: [' + "\n"
        h += '   { label: \'Desktop Visits\', data: ' + str(dta) + ',backgroundColor: \'#42c5f5\', }'
        h += '  ,{ label: \'Mobile Visits\', data: ' + str(dta_mobile) + ',backgroundColor: \'#42f5aa\', }'
        h += ']' + "\n"
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

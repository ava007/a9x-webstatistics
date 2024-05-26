# -*- coding: utf-8 -*-
import io, sys, argparse, json, ast
from copy import deepcopy
from datetime import datetime

def genHeader():
    h = '<hmtl>' + "\n"
    h += '<body>' + "\n"
    h += '<div> <canvas id="myChart"></canvas> </div>' + "\n"
    h += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>' + "\n"
    h += '<script> const ctx = document.getElementById(\'myChart\');' + "\n"
    return h
def runGenCockpit(infile):
    try:
        f = open(infile) 
    except FileNotFoundError: 
        print("-i file not found")
    try:
        d = json.load(f) 
    except json.JSONDecodeError:
        print("-i json file is not valid")

    lbl = []
    dta = []

    for e in d['days']:
        lbl.append(e)
        dta.append(d['days'][e]['device_hits']['desktop'])


    h = genHeader()
    h += 'new Chart(ctx, {'  + "\n"
    h += ' type: \'bar\',' 
    h += 'data: { ' + "\n" +  'labels: ' + str(lbl) + ',' + "\n"
    h += ' datasets: [{ label: \'User Visits\',  data: ' + str(dta) + ','
    h += '}]' + "\n"
    h += '}, });' + "\n"
    h += '</script></body></html>'

    print(h)

    exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False,
        prog='a9x_webstatistics',
        epilog="Version: "+ version('a9x-webstatistics')
    )
    parser.add_argument("-i", "--infile", help="json file that contains calculated statistics", default="webstat.json")
    args, unknown = parser.parse_known_args()

    runGenCockpit(infile=args.infile)

# -*- coding: utf-8 -*-
import io, sys, argparse, json, ast
from copy import deepcopy
from importlib.metadata import version
from datetime import datetime

def genHeader():
    h  = '<!doctype html><html lang="en"><head>' + "\n"
    h += '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">' + "\n"
    h += '<meta name="robots" content="index,follow">' + "\n"
    h += '</head>' + "\n"
    h += '<body>' + "\n"
    h += '<div><canvas id="myChart"></canvas></div>' + "\n"
    h += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>' + "\n"
    h += '<script>' + "\n" + 'const ctx = document.getElementById(\'myChart\');' + "\n"
    return h
    
def runGenCockpit(infile, outfile):
    with open(infile) as json_file:
        d = json.load(json_file) 

        lbl = []
        dta = []
        dta_mobile = []
        dta_tablet = []
        dta_bots = []

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
                if 'tablet' in d['days'][e]['device_hits']:
                    dta_tablet.append(d['days'][e]['device_hits']['tablet'])
                else:
                    dta_tablet.append(0)
                if 'bots' in d['days'][e]['device_hits']:
                    dta_bots.append(d['days'][e]['device_hits']['bots'])
                else:
                    dta_bots.append(0)
                # add "others" to "bots" in last element of the list:
                if 'others' in d['days'][e]['device_hits']:
                    dta_bots[-1] += d['days'][e]['device_hits']['others']
  
        except KeyError:
            print('KeyError occured!' + str(d['days'][e]) )
            raise

        h = genHeader()
        h += 'new Chart(ctx, {'  + "\n"
        h += ' responsive: true' + "\n"
        h += ' ,options: { scales: {x:{ stacked: true}, y:{ stacked: true } }' + "\n"
        h += ' ,plugins: { subtitle: { display: true, text: \'Hits per Device Class as of ' + d['timelastrec'][0:8] + ' ' + d['timelastrec'][8:6] + '\'} }' + "\n"
        h +=  ' },' + "\n"
        h += ' data: { ' + "\n" 
        h += '   datasets: [' + "\n"
        h += '      { type: \'line\',label: \'bots and others\',data: ' + str(dta_bots) + '}' + "\n"
        h += '     ,{ type: \'bar\', label: \'Desktop\', data: ' + str(dta) + ',backgroundColor: \'#42c5f5\'}' + "\n"
        h += '     ,{ type: \'bar\', label: \'Mobile\',  data: ' + str(dta_mobile) + ',backgroundColor: \'#42f5aa\'}' + "\n"
        h += '     ,{ type: \'bar\', label: \'Tablets\', data: ' + str(dta_tablet) + ',backgroundColor: \'#f5a742\'}' + "\n"
        h += '    ],' + "\n"
        h += '    labels: ' + str(lbl) + "\n"
        h += ' },' + "\n" + '});' + "\n"
        h += '</script>' + "\n"

        h += '<h2>Quality</h2>' + "\n"
        h += '<p>'
        h += '</p>' + "\n"
        
        h += '</body></html>'

        

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

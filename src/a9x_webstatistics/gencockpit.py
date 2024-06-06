# -*- coding: utf-8 -*-
import io, sys, argparse, json, ast
from operator import itemgetter
from copy import deepcopy
from importlib.metadata import version
from datetime import datetime

def genHeader():
    h  = '<!doctype html><html lang="en"><head>'
    h += '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    h += '<meta name="robots" content="index,follow">'
    h += '<style>'
    h += '* { font-family: "\'Helvetica Neue\', \'Helvetica\', \'Arial\', sans-serif";'
    h += '    font-size: 12px; }'
    h += '</style>'
    h += '</head>' + "\n"
    h += '<body>'
    h += '<div><canvas id="myChart"></canvas></div>'
    h += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
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

        h += '<h2>Top URL</h2>' + "\n"
        h += '<p><pre>'
        for k, v in reversed(d['days'].items()):
            h += str(k) + ": " + str(v) + "\n"
            h += str(v['source'])
        
        h += '</pre></p>' + "\n"

        # Top Countries
        actualYearMonth = datetime.today().strftime('%Y%m')
        tcountries = []
        for y in d['days']:
            currYearMonth = y[0:6]
            if currYearMonth == actualYearMonth:
               for c in d['days'][y]['countries']:
                   if c not in tcountries:
                       tcountries[c] = 0
                   tcountries[c] += c[0]
        h += '<h2>Top Countries</h2>' + "\n"
        h += '<p><table>'
        #for k, v in sorted(tcountries.items(), key=lambda x:x[0].lower(), reverse=True):
        #       for k, v in reversed(sorted(tcountries.keys())):
        
        # files = {"d":2, "g":1, "a":3, "b":3, "t":2}
        # print(files.items())
        #for k, v in sorted(list(tcountries.items()), key=lambda x:x[1].lower(), reverse=True):

        print("tcountries: " + str(tcountries))
        for k, v in sorted(tcountries, key=itemgetter(2), reverse=True):
             h += '<tr><td>' + str(k) + "</td><td>" + str(v) + "</td></tr>"
        h += '</table></p>' + "\n"
      
        
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

# -*- coding: utf-8 -*-
import io, sys, argparse, json, ast
from operator import itemgetter
from copy import deepcopy
from importlib.metadata import version
from datetime import datetime

def genHeader():
    h  = '<!doctype html><html lang="en"><head>'
    h += '<title>Web Statistics and Analysis</title>'
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
        h += '<h1>Analysis and Statistics of the last Days</h1>'
        h += 'new Chart(ctx, {'  + "\n"
        h += ' responsive: true' + "\n"
        h += ' ,options: { scales: {x:{ stacked: true}, y:{ stacked: true } }' + "\n"
        h += ' ,plugins: { subtitle: { display: true, text: \'Hits per Device Class as of ' + d['timelastrec'][0:8] + ' ' + d['timelastrec'][:-6] + '\'} }' + "\n"
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

        lastDate = list(d['days'].keys())[-1]
        actYearMonth = lastDate[0:6]
        
        tquality = {}   # nested dictionary!
        for k, v in sorted(d['days'].items(), key=itemgetter(0), reverse=True):
            curYearMonth = k[0:6]
            if curYearMonth == actYearMonth:
                if 'quality' in d['days'][k]:
                    for sk,sv in d['days'][k]['quality'].items():
                        print('sk: ' + str(sk) + ' sv: ' + str(sv))
                        if sk not in tquality:
                            tquality[sk] = {}
                            tquality[sk]['count'] = 1
                            tquality[sk]['status'] = sv['status']
                            tquality[sk]['from'] = sv['from']
                            tquality[sk]['comment'] = sv['comment']
                        else:
                            tquality[sk]['count']  += 1

        if len(tquality) > 0:
            h += '<h2>Quality Improvements</h2>'
            h += '<table><thead><tr><th scope="col">affected URL</th><th scope="col">Status</th><th scope="col">affected URL is called by</th><th scope="col">Count</th><th scope="col">Remark</th></tr></thead>'
            i = 0
            for k, v in sorted(tquality.items(), key=lambda x: (x[1]['count']), reverse=True):
                h += '<tr><td>' + str(k) + "</td><td>" + str(v['status']) + "</td>"
                h += '<td>' + v['from'] + "</td>"
                h += '<td>' + str(v['count']) + "</td>"
                h += '<td>' + v['comment'] + "</td></tr>"
                i += 1
                if i == 5:
                    break
            h += '</table>' + "\n"

        # Top Sources
        tsource = {}
        for y in d['days']:
            curYearMonth = y[0:6]
            if curYearMonth == actYearMonth:
                if 'source' in d['days'][y]:
                    for sk,sv in d['days'][y]['source'].items():
                        if sk not in tsource:
                            tsource[sk] = 0
                        tsource[sk] += sv

        h += '<h2>Top 5 Sources</h2>'
        h += '<table>'
        h += '<thead><tr><th scope="col">Source Domain</th><th scope="col">Source Hits</th></tr></thead>'
        i = 0
        for k, v in sorted(tsource.items(), key=itemgetter(1), reverse=True):
             h += '<tr><td>' + str(k) + "</td><td>" + str(v) + "</td></tr>"
             i += 1
             if i == 5:
                 break
        h += '</table>' + "\n"

        #for k, v in reversed(d['days'].items()):
        #    if 'source' in d['days'][k]:
        #        for sk, sv in d['days'][k]['source'].items():

        # Top Countries
        tcountries = {}
        for y in d['days']:
            curYearMonth = y[0:6]
            print (curYearMonth + " " + actYearMonth)
            if curYearMonth == actYearMonth:
               for co,cv in d['days'][y]['countries'].items():
                   if co not in tcountries:
                       tcountries[co] = 0
                   tcountries[co] += cv

        if len(tcountries) > 0:
            h += '<h2>Top 5 Countries</h2>' + "\n"
            h += '<table>'
            h += '<thead><tr><th scope="col">Source Country</th><th scope="col">Source Hits</th></tr></thead>'
            i = 0
            for k, v in sorted(tcountries.items(), key=itemgetter(1), reverse=True):
                h += '<tr><td>' + str(k) + "</td><td>" + str(v) + "</td></tr>"
                i += 1
                if i == 5:
                    break
            h += '</table>' + "\n"

        h += '<footer>'
        h += '<a href="https://github.com/ava007/a9x-webstatistics">License and Copyright</a>'
        h += '</footer>'
        
        
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

# -*- coding: utf-8 -*-
import io, sys, argparse, json, ast
from operator import itemgetter
from copy import deepcopy
from importlib.metadata import version
from datetime import datetime, timedelta

def genHeader():
    h  = '<!doctype html><html lang="en"><head>'
    h += '<title>Web Statistics and Analysis</title>'
    h += '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    h += '<meta name="robots" content="index,follow">'
    h += '<style>'
    h += '* { font-family: "\'Helvetica Neue\', Helvetica, Arial, sans-serif"; font-size: 12px; }'
    h += '.flex-container { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: flex-start; align-items: flex-start; }'
    h += '.flex-item { background: tomato; padding: 14px; margin-top: 10px; margin-right: 10px; color: white; }'
    h += '</style>'
    h += '</head>' + "\n"
    h += '<body>'
    return h
    
def runGenCockpit(infile, outfile, domain):
    with open(infile) as json_file:
        d = json.load(json_file) 

        day_lbl = []
        day_dta_desktop = []
        day_dta_mobile = []
        day_dta_tablet = []
        day_dta_bots = []
        day_dta_visits = []

        day_dta_i = 0
        try:
            for k, v in sorted(d['days'].items(), key=itemgetter(0), reverse=True):
                # show at max 31 days:
                if day_dta_i > 31:
                    break
                # consider only days:
                if len(k) < 8:
                    continue
                day_dta_i += 1
                day_lbl.append(k)
                if 'desktop' in d['days'][k]['device_hits']:
                    day_dta_desktop.append(d['days'][k]['device_hits']['desktop'])
                else:
                    day_dta_desktop.append(0)
                if 'mobile' in d['days'][k]['device_hits']:
                    day_dta_mobile.append(d['days'][k]['device_hits']['mobile'])
                else:
                    day_dta_mobile.append(0)
                if 'tablet' in d['days'][k]['device_hits']:
                    day_dta_tablet.append(d['days'][k]['device_hits']['tablet'])
                else:
                    day_dta_tablet.append(0)
                if 'bots' in d['days'][k]['device_hits']:
                    day_dta_bots.append(d['days'][k]['device_hits']['bots'])
                else:
                    day_dta_bots.append(0)
                # add "others" to "bots" in last element of the list:
                if 'others' in d['days'][k]['device_hits']:
                    day_dta_bots[-1] += d['days'][k]['device_hits']['others']
                    
                # visits:
                if 'visits' in d['days'][k]:
                    day_dta_visits.append(d['days'][k]['visits'])
                else:
                    day_dta_visits.append(0)
  
        except KeyError:
            print('KeyError occured! ' + str(d['days'][k]) )
            raise

        day_lbl.reverse()
        day_dta_desktop.reverse()
        day_dta_mobile.reverse()
        day_dta_tablet.reverse()
        day_dta_bots.reverse()

        h = genHeader()
        h += '<h1>Analysis and Statistics of the last Days</h1>'
        h += '<div><canvas id="myChart"></canvas></div>'
        h += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
        h += '<script>' + "\n" + 'const ctx = document.getElementById(\'myChart\');' + "\n"
        h += 'new Chart(ctx, {'  + "\n"
        h += ' responsive: true' + "\n"
        h += ' ,options: { scales: {x:{ stacked: true}, y:{ stacked: true } }' + "\n"
        h += ' ,plugins: { subtitle: { display: true, text: \'Hits per Device Class as of ' + d['timelastrec'][0:8] + ' ' + d['timelastrec'][-6:] + '\'} }' + "\n"
        h +=  ' },' + "\n"
        h += ' data: { ' + "\n" 
        h += '   datasets: [' + "\n"
        h += '      { type: \'line\',label: \'bots and others\',data: ' + str(day_dta_bots) + '}' + "\n"
        h += '     ,{ type: \'line\',label: \'Visits\',  data: ' + str(day_dta_visits)  + ',backgroundColor: \'#ff0000\'}' + "\n"
        h += '     ,{ type: \'bar\', label: \'Desktop\', data: ' + str(day_dta_desktop) + ',backgroundColor: \'#42c5f5\'}' + "\n"
        h += '     ,{ type: \'bar\', label: \'Mobile\',  data: ' + str(day_dta_mobile) + ',backgroundColor: \'#42f5aa\'}' + "\n"
        h += '     ,{ type: \'bar\', label: \'Tablets\', data: ' + str(day_dta_tablet) + ',backgroundColor: \'#f5a742\'}' + "\n"
        h += '    ],' + "\n"
        h += '    labels: ' + str(day_lbl) + "\n"
        h += ' },' + "\n" + '});' + "\n"
        h += '</script>' + "\n"

        lastDate = list(d['days'].keys())[-1]
        actYearMonth = lastDate[0:6]
        
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

        h += '<div class="flex-container">'
        h += '<div class="flex-item">'
        h += '<h2>Top 10 Sources by Domain</h2>'
        h += '<table>'
        h += '<thead><tr><th scope="col" style="text-align: left">Domain</th><th scope="col">Hit Count</th></tr></thead>'
        i = 0
        for k, v in sorted(tsource.items(), key=itemgetter(1), reverse=True):
             h += '<tr><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
             i += 1
             if i == 10:
                 break
        h += '</table></div>'  + "\n"

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
            h += '<div class="flex-item">'
            h += '<h2>Top 10 Countries</h2>' + "\n"
            h += '<table>'
            h += '<thead><tr><th scope="col" style="text-align: left">Country</th><th scope="col">Hit Count</th></tr></thead>'
            i = 0
            for k, v in sorted(tcountries.items(), key=itemgetter(1), reverse=True):
                h += '<tr><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                i += 1
                if i == 10:
                    break
            h += '</table></div>' + "\n"

        # top urls for the last 31 days:
        ttopurl = {}
        topurlcnt = 0
        for k, v in sorted(d['days'].items(), key=itemgetter(0), reverse=True):
            if topurlcnt >= 31:
                break
            topurlcnt += 1
            if 'topurl' in d['days'][k]:
                for tk, tv in d['days'][k]['topurl'].items():
                    if tk not in ttopurl:
                        ttopurl[tk] = 0
                    ttopurl[tk] += tv
        if len(ttopurl) > 0:
            h += '<div class="flex-item">'
            h += '<h2>Top 10 URLs for last ' + str(topurlcnt) + ' Days</h2>'
            h += '<table>'
            h += '<thead><tr><th scope="col" style="text-align: left">URL</th><th scope="col">Hit Count</th></tr></thead>'
            i = 0
            for k, v in sorted(ttopurl.items(), key=itemgetter(1), reverse=True):
                if not k.endswith('.css') and not k.endswith('.json') and not k.endswith('.ico'):
                    h += '<tr><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                    i += 1
                if i == 10:
                    break
            h += '</table></div>' + "\n"
                    
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
                            tquality[sk]['lastoccured'] = k
                        else:
                            tquality[sk]['count']  += 1

        if len(tquality) > 0:
            h += '<div class="flex-item">'
            h += '<h2>Possible Quality Improvements</h2>'
            h += '<table><thead><tr><th scope="col" style="text-align: left">affected URL</th><th scope="col">Status</th><th scope="col" style="text-align: left">affected URL is called by</th><th scope="col">Count</th><th scope="col">Remark</th><th scope="col">Date last occured</th></tr></thead>'
            i = 0
            for k, v in sorted(tquality.items(), key=lambda x: (x[1]['count']), reverse=True):
                h += '<tr><td>' + str(k) + "</td><td>" + str(v['status']) + '</td>'
                h += '<td>' + v['from'] + '</td>'
                h += '<td style="text-align: right">' + str(format(v['count'],',')) + '</td>'
                h += '<td>' + v['comment'] + '</td>'
                h += '<td>' + v['lastoccured'] + '</td>'
                h += '</tr>'
                i += 1
                if i == 10:
                    break
            h += '</table></div>' + "\n"
       
        # top external landings (friends):
        tland = {}   # nested dictionary!
        firstOfCurrentMonth =  actYearMonth + '01'
        if firstOfCurrentMonth in d['days'] and 'friends' in d['days'][firstOfCurrentMonth]:
            h += '<div class="flex-item">'
            h += '<h2>Top 10 Landings from Friends</h2>' + "\n"
            h += '<table><thead><tr><th scope="col" style="text-align: left">Source</th><th scope="col">Target</th><th scope="col" style="text-align: left">Count</th></tr></thead>'
            for k, v in sorted(d['days'][firstOfCurrentMonth]['friends'].items(), key=itemgetter(0), reverse=True):
                for kb, vb in v['target'].items():
                    h += '<tr><td>' + k + '</td><td>' + str(kb) + '</td><td>' + str(vb) + '</td></tr>'
            h += '</table></div>'  + "\n"
        
        h += '</div>' + "\n"

        
        # Webstatistics for the last months
        tlr = datetime.strptime(d['timelastrec'] + " +0000","%Y%m%d%H%M%S %z")
        tlr_first = tlr.replace(day=1)
        tlr_last_month = tlr_first - timedelta(days=1)
        print("Last month: " + tlr_last_month.strftime("%Y%m"))

        maxYearMonth = tlr_last_month.strftime("%Y%m")
        prevYearMonth = '999912'

        mth_lbl = []
        mth_dta_desktop = []
        mth_dta_mobile = []
        mth_dta_tablet = []
        mth_dta_bots = []
        mth_dta_visits = []

        # loop through month beginning with highest month:
        for k, v in sorted(d['days'].items(), key=itemgetter(0), reverse=True):
            curYearMonth = k[0:6]
            if curYearMonth <= maxYearMonth:
                if  curYearMonth != prevYearMonth:
                    prevYearMonth = curYearMonth
                    mth_lbl.append(curYearMonth)
                    mth_dta_desktop.append(0)
                    mth_dta_mobile.append(0)
                    mth_dta_tablet.append(0)
                    mth_dta_bots.append(0)
                    mth_dta_visits.append(0)
                    
                if 'desktop' in d['days'][k]['device_hits']:
                    mth_dta_desktop[-1] += d['days'][k]['device_hits']['desktop']
                if 'mobile' in d['days'][k]['device_hits']:
                    mth_dta_mobile[-1] += d['days'][k]['device_hits']['mobile']
                if 'tablet' in d['days'][k]['device_hits']:
                    mth_dta_tablet[-1] += d['days'][k]['device_hits']['tablet']
                if 'bots' in d['days'][k]['device_hits']:
                    mth_dta_bots[-1] += d['days'][k]['device_hits']['bots']
                # add "others" to "bots" in last element of the list:
                if 'others' in d['days'][k]['device_hits']:
                    mth_dta_bots[-1] += d['days'][k]['device_hits']['others']

                # visits:
                if 'visits' in d['days'][k]:
                    mth_dta_visits[-1] += d['days'][k]['visits']
             
        if len(mth_lbl) > 0:
            mth_lbl.reverse()
            mth_dta_desktop.reverse()
            mth_dta_mobile.reverse()
            mth_dta_tablet.reverse()
            mth_dta_bots.reverse()
            mth_dta_visits.reverse()
            h += '<h1>Webstatistics for the last Months</h1>'
            h += '<div><canvas id="a9x_ws_months"></canvas></div>'
            h += '<script>' + "\n" + 'const mth_ctx = document.getElementById(\'a9x_ws_months\');' + "\n"
            h += 'new Chart(mth_ctx, {'  + "\n"
            h += ' responsive: true' + "\n"
            h += ' ,options: { scales: {x:{ stacked: true}, y:{ stacked: true } }' + "\n"
            h += ' ,plugins: { subtitle: { display: true, text: \'Hits per Device Class as of ' + d['timelastrec'][0:8] + '\'} }' + "\n"
            h +=  ' },' + "\n"
            h += ' data: { ' + "\n" 
            h += '   datasets: [' + "\n"
            h += '      { type: \'line\',label: \'bots and others\',data: ' + str(mth_dta_bots) + '}' + "\n"
            h += '     ,{ type: \'line\',label: \'Visits\',  data: ' + str(mth_dta_visits) + ',backgroundColor: \'#ff0000\'}' + "\n"
            h += '     ,{ type: \'bar\', label: \'Desktop\', data: ' + str(mth_dta_desktop)+ ',backgroundColor: \'#42c5f5\'}' + "\n"
            h += '     ,{ type: \'bar\', label: \'Mobile\',  data: ' + str(mth_dta_mobile) + ',backgroundColor: \'#42f5aa\'}' + "\n"
            h += '     ,{ type: \'bar\', label: \'Tablets\', data: ' + str(mth_dta_tablet) + ',backgroundColor: \'#f5a742\'}' + "\n"
            h += '    ],' + "\n"
            h += '    labels: ' + str(mth_lbl) + "\n"
            h += ' },' + "\n" + '});' + "\n"
            h += '</script>' + "\n"

        h += '<div class="flex-container">'
        # Top Countries
        tcountries = {}
        tccount = 0
        # loop through month beginning with highest month:
        for k, v in sorted(d['days'].items(), key=itemgetter(0), reverse=True):
            if len(k) == 6:    
                if tccount > 12:
                    break
                tccount += 1
                for co,cv in d['days'][k]['countries'].items():
                    if co not in tcountries:
                        tcountries[co] = 0
                    tcountries[co] += cv

        if len(tcountries) > 0:
            h += '<div class="flex-item">'
            h += '<h2>Top 10 Countries</h2>'
            h += '<table>'
            h += '<thead><tr><th scope="col" style="text-align: left">Country</th><th scope="col">Hits count</th></tr></thead>'
            i = 0
            for k, v in sorted(tcountries.items(), key=itemgetter(1), reverse=True):
                h += '<tr><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                i += 1
                if i == 10:
                    break
            h += '</table></div>' + "\n"

        # top urls
        ttopurl = {}
        topurlcnt = 0
        for k, v in sorted(d['days'].items(), key=itemgetter(0), reverse=True):
            if len(k) == 6:    
                if topurlcnt > 12:
                    break
                topurlcnt += 1
                if 'topurl' in d['days'][k]:
                    for tk, tv in d['days'][k]['topurl'].items():
                        if tk not in ttopurl:
                            ttopurl[tk] = 0
                        ttopurl[tk] += tv
        if len(ttopurl) > 0:
            h += '<div class="flex-item">'
            h += '<h2>Top 10 URL</h2>'
            h += '<table>'
            h += '<thead><tr><th scope="col">URL</th><th scope="col">Hit Count</th></tr></thead>'
            i = 0
            for k, v in sorted(ttopurl.items(), key=itemgetter(1), reverse=True):
                if not k.endswith('.css') and not k.endswith('.json') and not k.endswith('.ico'):
                    h += '<tr><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                    i += 1
                if i == 10:
                    break
            h += '</table></div>' + "\n"
        h += '</div>' + "\n"

        h += '<footer>'
        h += '<a href="https://github.com/ava007/a9x-webstatistics">License and Copyright</a>'
        h += '<pre>URL: Uniform Resource Locator</pre>'
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
    parser.add_argument("-d", "--domain", help="domain https://logikfabrik.com on which the access log file runs", default="https://logikfabrik.com")
    args, unknown = parser.parse_known_args()

    runGenCockpit(infile=args.infile, outfile=args.outfile, domain=args.domain)

# -*- coding: utf-8 -*-
import io, sys, argparse, json, ast
from operator import itemgetter
from copy import deepcopy
from importlib.metadata import version
from datetime import datetime, timedelta

def genHeaderV0001(domain):
    h  = '<!doctype html><html lang="en"><head>'
    h += '<title>Web Statistics and Analysis for ' + domain + '</title>'
    h += '<meta name="viewport" content="width=device-width, initial-scale=1">'
    h += '<meta charset="utf-8">'
    h += '<meta name="robots" content="index,follow">'
    h += '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">'
    #h += '<style>'
    #h += '* { font-family: "\'Helvetica Neue\', Helvetica, Arial, sans-serif"; font-size: 12px; }'
    #h += '.flex-container { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: flex-start; align-items: flex-start; }'
    #h += '.flex-item { background: tomato; padding: 14px; margin-top: 10px; margin-right: 10px; color: white; }'
    #h += '</style>'
    #h += '</head>' + "\n"
    h += '<body>'
    h += '<div class="container">'
    h += '<h1>Web Analytics and Statistics for ' + domain + '</h1>'
    return h
    
def runGenCockpitV0001(infile, outfile, domain):

    owndomain = domain.replace('http://','')
    owndomain = owndomain.replace('https://','')
    owndomain = owndomain.replace('www.','')
    
    with open(infile) as json_file:
        d = json.load(json_file) 

        day_lbl = []
        day_usr_desktop = []
        day_usr_mobile = []
        day_usr_tablet = []
        day_usr_visits = []
        day_robot_hits = []

        day_usr_i = 0
        try:
            for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
                # consider only days:
                if len(k) < 8:
                    continue
                # show at max 31 days:
                if day_usr_i > 31:
                    break
                day_usr_i += 1
                day_lbl.append(k)
                if 'desktop' in d['v0001']['days'][k]['user']['deviceHits']:
                    day_usr_desktop.append(d['v0001']['days'][k]['user']['deviceHits']['desktop'])
                else:
                    day_usr_desktop.append(0)
                if 'mobile' in d['v0001']['days'][k]['user']['deviceHits']:
                    day_usr_mobile.append(d['v0001']['days'][k]['user']['deviceHits']['mobile'])
                else:
                    day_usr_mobile.append(0)
                if 'tablet' in d['v0001']['days'][k]['user']['deviceHits']:
                    day_usr_tablet.append(d['v0001']['days'][k]['user']['deviceHits']['tablet'])
                else:
                    day_usr_tablet.append(0)
                if 'robotHits' in d['v0001']['days'][k]['robot']:
                    day_robot_hits.append(d['v0001']['days'][k]['robot']['robotHits'])
                else:
                    day_robot_hits.append(0)
                                    
                # visits:
                if 'visits' in d['v0001']['days'][k]['user']:
                    day_usr_visits.append(d['v0001']['days'][k]['user']['visits'])
                else:
                    day_usr_visits.append(0)
  
        except KeyError:
            print('KeyError occured! ' + str(d['v0001']['days'][k]) )
            raise

        day_lbl.reverse()
        day_usr_desktop.reverse()
        day_usr_mobile.reverse()
        day_usr_tablet.reverse()
        day_robot_hits.reverse()
        day_usr_visits.reverse()

        h = genHeaderV0001(owndomain)
        h += '<p><small>Last record included in statistic: ' + d['timelastrec'][0:8] + " " + d['timelastrec'][-6:] + '</small></p>'
        h += '<h2>Analysis and Statistics of the 31 Days</h2>'
        h += '<div class="row">'
        h += '<div><canvas id="myChart"></canvas></div>'
        h += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
        h += '<script>' + "\n" + 'const ctx = document.getElementById(\'myChart\');' + "\n"
        h += "const dctx = new Chart(ctx, {"  + "\n"
        h += " type: 'bar', "  
        h += " options: { responsive: true, scales: {"
        h += "    x: { stacked: true,  ticks: { beginAtZero: true } }, "
        h += "    y: { stacked: true,  ticks: { beginAtZero: true } }, "
        h += "    y2: { stacked: false, ticks: {beginAtZero: true}, position: 'right'}"
        h += "  } }" + "\n"
        h += " ,plugins: { subtitle: { display: true, text: 'Hits per Device Class as of " + d['timelastrec'][0:8] + " " + d['timelastrec'][-6:] + "'} }" + "\n"
        h += " ,data: { " + "\n" 
        h += "   datasets: [" + "\n"
        h += "     { type: 'line',label: 'Robots', data: " + str(day_robot_hits) + ", yAxisID: 'y2', order:1}" + "\n"
        h += "    ,{ type: 'bar', label: 'User - Desktop', data: " + str(day_usr_desktop) + " ,backgroundColor: '#42c5f5', order:3}" + "\n"
        h += "    ,{ type: 'bar', label: 'User - Mobile',  data: " + str(day_usr_mobile) + " ,backgroundColor: '#42f5aa', order:4}" + "\n"
        h += "    ,{ type: 'bar', label: 'User - Tablet', data: " + str(day_usr_tablet) + " ,backgroundColor: '#f5a742', order:5}" + "\n"
        h += "    ,{ type: 'line',label: 'User Visit', data: " + str(day_usr_visits)  + " ,backgroundColor: '#ff0000', borderColor: '#ff0000', tension: 0.1, yAxisID: 'y2', order: 2}" + "\n"
        h += "    ]," + "\n"
        h += "    labels: " + str(day_lbl) + "\n"
        h += " }," + "\n" + "});" + "\n"
        h += "var xmax = 0; "
        h += "var tmax = 0;" + "\n"
        h += "for (i=0; i<5; i++) {" 
        h += "  tmax = Math.max.apply(null, dctx.data.datasets[i].data); "
        h += "  if (tmax > xmax) {  xmax = tmax; } " 
        h += "}" + "\n"
        h += "dctx.options.scales.y.max = xmax + 5;" + "\n"
        h += "dctx.options.scales.y2.max = xmax + 5;" + "\n"
        h += "dctx.update();" + "\n"
        h += '</script>' + "\n"
        h += '</div>'  # end of row
        

        lastDate = list(d['v0001']['days'].keys())[-1]
        actYearMonth = lastDate[0:6]
        
        # Top 10 Domains on daily basis
        tsource = {}
        for y in d['v0001']['days']:
            curYearMonth = y[0:6]
            if curYearMonth == actYearMonth:
                if 'externalFriendsHits' in d['v0001']['days'][y]['user']:
                    for sk,sv in d['v0001']['days'][y]['user']['externalFriendsHits'].items():
                        if sk not in tsource:
                            tsource[sk] = 0
                        tsource[sk] += sv['cnt']

        h += '<div class="row">'
        h += '<div class="col text-bg-info">'
        h += '<h3>Top 10 Domains</h3>'
        h += '<p><small>Incoming traffic (user hits) for the last 31 days by external source domain</small></p>'
        h += '<table class="table">'
        h += '<thead><tr><th scope="col" style="text-align: left">Domain</th><th scope="col">Hit Count</th></tr></thead>'
        i = 0
        for k, v in sorted(tsource.items(), key=itemgetter(1), reverse=True):
             if owndomain in k:
                 continue
             h += '<tr><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
             i += 1
             if i == 10:
                 break
        h += '</table>'
        h += '</div>'  + "\n"   # end of col

        # Top Countries
        tcountries = {}
        for y in d['v0001']['days']:
            curYearMonth = y[0:6]
            #print (curYearMonth + " " + actYearMonth)
            if curYearMonth == actYearMonth:
                try:
                    for co,cv in d['v0001']['days'][y]['user']['countryHits'].items():
                        if co not in tcountries:
                            tcountries[co] = 0
                        tcountries[co] += cv
                except KeyError: 
                    print ('ERROR: topcountries: key not found!' + str(d['v0001']['days'][y]['user']))
                    continue
        
        if len(tcountries) > 0:
            h += '<div class="col">'
            h += '<h3>Top 10 Countries</h3>' + "\n"
            h += '<p><small>User hits for the last 31 days by country</small></p>'
            h += '<table class="table">'
            h += '<thead><tr><th>Rank</th><th scope="col" style="text-align: left">Country</th><th scope="col">Hit Count</th></tr></thead>'
            i = 1
            for k, v in sorted(tcountries.items(), key=itemgetter(1), reverse=True):
                h += '<tr><td>' +str(i) + '</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                i += 1
                if i > 10:
                    break
            h += '</table>'
            h += '</div>'  + "\n"   # end of col


        # top urls for the last 31 days:
        ttopurl = {}
        topurlcnt = 0
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            # dont take months in account:
            if len(k) <= 6:
                continue
            if topurlcnt >= 31:
                break
            topurlcnt += 1
            if 'topUrl' in d['v0001']['days'][k]['user']:
                for tk, tv in d['v0001']['days'][k]['user']['topUrl'].items():
                    if tk not in ttopurl:
                        ttopurl[tk] = 0
                    ttopurl[tk] += tv
        if len(ttopurl) > 0:
            h += '<div class="col">'
            h += '<h3>Top 10 URLs</h3>'
            h += '<p><small>User hits for the last ' + str(topurlcnt) + ' days by internal URL on ' + owndomain + '</small></p>'
            h += '<table class="table">'
            h += '<thead><tr><th scope="col" style="text-align: left">URL</th><th scope="col">Hit Count</th></tr></thead>'
            i = 0
            for k, v in sorted(ttopurl.items(), key=itemgetter(1), reverse=True):
                if not k.endswith('.css') and not k.endswith('.json') and not k.endswith('.ico'):
                    h += '<tr><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                    i += 1
                if i == 10:
                    break
            h += '</table>'
            h += '</div>'  + "\n"   # end of col
       
        # top external landings (friends):
        tland = {}   # nested dictionary!
        firstOfCurrentMonth =  actYearMonth + '01'
        if firstOfCurrentMonth in d['v0001']['days'] and 'externalFriendsHits' in d['v0001']['days'][firstOfCurrentMonth]['user']:
            h += '<div class="col">'
            h += '<h3>Top 10 Landings</h3>' + "\n"
            h += '<p><small>User landing for the last 31 days</small></p>'
            h += '<table><thead><tr><th scope="col" style="text-align: left">Source</th><th scope="col">Target</th><th scope="col" style="text-align: left">Count</th></tr></thead>'
            for k, v in sorted(d['v0001']['days'][firstOfCurrentMonth]['user']['externalFriendsHits'].items(), key=itemgetter(0), reverse=True):
                for kb, vb in v['target'].items():
                    if owndomain not in k:
                        h += '<tr><td>' + k + '</td><td>' + str(kb) + '</td><td>' + str(vb) + '</td></tr>'
            h += '</table>'
            h += '</div>'  + "\n"   # end of col

        tquality = {}   # nested dictionary!
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            curYearMonth = k[0:6]
            if curYearMonth == actYearMonth:
                if 'quality' in d['v0001']['days'][k]:
                    for sk,sv in d['v0001']['days'][k]['quality'].items():
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
            h += '<div class="col">'
            h += '<h3>Possible Quality Improvements</h3>'
            h += '<table class="table"><thead><tr><th scope="col" style="text-align: left">affected URL</th><th scope="col">Status</th><th scope="col" style="text-align: left">affected URL is called by</th><th scope="col">Count</th><th scope="col">Remark</th><th scope="col">Date last occured</th></tr></thead>'
            i = 0
            for k, v in sorted(tquality.items(), key=lambda x: (x[1]['lastoccured']), reverse=True):
                h += '<tr><td>' + str(k) + "</td><td>" + str(v['status']) + '</td>'
                h += '<td>' + v['from'] + '</td>'
                h += '<td style="text-align: right">' + str(format(v['count'],',')) + '</td>'
                h += '<td>' + v['comment'] + '</td>'
                h += '<td>' + v['lastoccured'] + '</td>'
                h += '</tr>'
                i += 1
                if i == 10:
                    break
            h += '</table>'
            h += '</div>'  + "\n"   # end of col
        
        h += '</div>' + "\n"   # end of row
        
        # Webstatistics for the last months
        tlr = datetime.strptime(d['timelastrec'] + " +0000","%Y%m%d%H%M%S %z")
        tlr_first = tlr.replace(day=1)
        tlr_last_month = tlr_first - timedelta(days=1)
        print("webstats last months; last is month: " + tlr_last_month.strftime("%Y%m"))

        maxYearMonth = tlr_last_month.strftime("%Y%m")
        prevYearMonth = '999912'

        mth_lbl = []
        mth_usr_desktop = []
        mth_usr_mobile = []
        mth_usr_tablet = []
        mth_usr_bots = []
        mth_usr_visits = []

        # loop through month beginning with highest month:
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            curYearMonth = k[0:6]
            if curYearMonth <= maxYearMonth:
                if  curYearMonth != prevYearMonth:
                    prevYearMonth = curYearMonth
                    mth_lbl.append(curYearMonth)
                    mth_usr_desktop.append(0)
                    mth_usr_mobile.append(0)
                    mth_usr_tablet.append(0)
                    mth_usr_bots.append(0)
                    mth_usr_visits.append(0)
                    
                if 'desktop' in d['v0001']['days'][k]['user']['deviceHits']:
                    mth_usr_desktop[-1] += d['v0001']['days'][k]['user']['deviceHits']['desktop']
                if 'mobile' in d['v0001']['days'][k]['user']['deviceHits']:
                    mth_usr_mobile[-1] += d['v0001']['days'][k]['user']['deviceHits']['mobile']
                if 'tablet' in d['v0001']['days'][k]['user']['deviceHits']:
                    mth_usr_tablet[-1] += d['v0001']['days'][k]['user']['deviceHits']['tablet']
                if 'robot' in d['v0001']['days'][k]['user']['deviceHits']:
                    mth_usr_bots[-1] += d['v0001']['days'][k]['user']['deviceHits']['robot']

                # visits:
                if 'visits' in d['v0001']['days'][k]['user']:
                    mth_usr_visits[-1] += d['v0001']['days'][k]['user']['visits']
        
        ## Months:   
        if len(mth_lbl) > 0:
            mth_lbl.reverse()
            mth_usr_desktop.reverse()
            mth_usr_mobile.reverse()
            mth_usr_tablet.reverse()
            mth_usr_bots.reverse()
            mth_usr_visits.reverse()
            h += '<h2>Webstatistics for the last Months for ' + owndomain + '</h2>'
            h += '<div><canvas id="a9x_ws_months"></canvas></div>'
            h += "<script>" + "\n" + "const mth_ctx = document.getElementById('a9x_ws_months');" + "\n"
            h += "const mctx = new Chart(mth_ctx, {"  + "\n"
            h += "  options: { responsive: true, scales: {x:{ stacked: true}, y:{ stacked: true }, y2: { stacked: false, position: 'right'} }}" + "\n"
            h += " ,plugins: { subtitle: { display: true, text: 'Hits per Device Class as of " + d['timelastrec'][0:8] + "'} }" + "\n"
            h += " ,data: { " + "\n" 
            h += "   datasets: [" + "\n"
            h += "      { type: 'bar', label: 'User - Desktop', data: " + str(mth_usr_desktop)+ ", backgroundColor: '#42c5f5', order: 3}" + "\n"
            h += "     ,{ type: 'bar', label: 'User - Mobile',  data: " + str(mth_usr_mobile) + ", backgroundColor: '#42f5aa', order: 4}" + "\n"
            h += "     ,{ type: 'bar', label: 'User - Tablet', data: " + str(mth_usr_tablet) + ", backgroundColor: '#f5a742', order: 5}" + "\n"
            h += "     ,{ type: 'line',label: 'Robots', data: " + str(mth_usr_bots) + ", yAxisID: 'y2', order: 2}" + "\n"
            h += "     ,{ type: 'line',label: 'User - Visit',  data: " + str(mth_usr_visits) + ",backgroundColor: '#ff0000', borderColor: '#ff0000', tension: 0.1, yAxisID: 'y2', order: 1}" + "\n"
            h += "    ]," + "\n"
            h += "    labels: " + str(mth_lbl) + "\n"
            h += " }," + "\n" + "});" + "\n"
            h += "var xmax = 0; "
            h += "var tmax = 0;" + "\n"
            h += "for (i=0; i<5; i++) {" 
            h += "  tmax = Math.max.apply(null, mctx.data.datasets[i].data); "
            h += "  if (tmax > xmax) {  xmax = tmax; } " 
            h += "}" + "\n"
            h += "mctx.options.scales.y.max = xmax + 5;" + "\n"
            h += "mctx.options.scales.y2.max = xmax + 5;" + "\n"
            h += "mctx.update();" + "\n"
            h += "</script>" + "\n"

        # Top 10 Domains on monthly basis
        tsource = {}
        for y in d['v0001']['days']:
            curYearMonth = y[0:6]
            if 'externalFriendsHits' in d['v0001']['days'][y]['user']:
                for sk,sv in d['v0001']['days'][y]['user']['externalFriendsHits'].items():
                    if sk not in tsource:
                        tsource[sk] = 0
                    tsource[sk] += sv['cnt']
        h += '<div class="card mt-2">'
        h += '<div class="card-body">'
        h += '<h3 class="card-title">Top 10 Domains</h3>'
        h += '<h4 class="card-subtitle mb-2 text-body-secondary">Hit list of domains where traffic comes from.</h4>'
        h += '<p class="card-text">'
        h += '<table class="table">'
        h += '<thead><tr><th scope="col" style="text-align: left">Domain</th><th scope="col">Hit Count</th></tr></thead>'
        i = 0
        for k, v in sorted(tsource.items(), key=itemgetter(1), reverse=True):
             if owndomain in k:
                 continue
             h += '<tr><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
             i += 1
             if i == 10:
                 break
        h += '</table></div>'  + "\n"
        
        
        h += '<div class="col">'
        # Top Countries
        tcountries = {}
        tccount = 0
        # loop through month beginning with highest month:
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            if len(k) == 6:    
                if tccount > 12:
                    break
                tccount += 1
                for co,cv in d['v0001']['days'][k]['user']['countryHits'].items():
                    if co not in tcountries:
                        tcountries[co] = 0
                    tcountries[co] += cv

        if len(tcountries) > 0:
            h += '<div class="card mt-2">'
            h += '<div class="card-body">'
            h += '<h3 class="card-title">Top 10 Coutries</h3>'
            h += '<h4 class="card-subtitle mb-2 text-body-secondary">Hit list of countries giving the most hits.</h4>'
            h += '<p class="card-text">'
            h += '<table class="table">'
            h += '<thead><tr><th scope="col" style="text-align: left">Country</th><th scope="col">Hits count</th></tr></thead>'
            i = 0
            for k, v in sorted(tcountries.items(), key=itemgetter(1), reverse=True):
                h += '<tr><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                i += 1
                if i == 10:
                    break
            h += '</table></p></div></div>' + "\n"

        # top urls
        ttopurl = {}
        topurlcnt = 0
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            if len(k) == 6:    
                if topurlcnt > 12:
                    break
                topurlcnt += 1
                if 'topUrl' in d['v0001']['days'][k]['user']:
                    for tk, tv in d['v0001']['days'][k]['user']['topUrl'].items():
                        if tk not in ttopurl:
                            ttopurl[tk] = 0
                        ttopurl[tk] += tv
        if len(ttopurl) > 0:
            h += '<div class="card text-bg-info mt-2">'
            h += '<div class="card-body">'
            h += '<h3 class="card-title">Top 10 URL</h3>'
            h += '<h4 class="card-subtitle mb-2 text-body-secondary">URL with the most hits.</h4>'
            h += '<p class="card-text">'
            h += '<table class="table table-info">'
            h += '<thead><tr><th scope="col">Rank</th><th scope="col">URL</th><th scope="col">Hit Count</th></tr></thead>'
            i = 1
            vdomain = domain.replace('https://','')
            vdomain = vdomain.replace('http://','')
            vdomain = vdomain.removeprefix('www.')
            for k, v in sorted(ttopurl.items(), key=itemgetter(1), reverse=True):
                if not k.endswith('.css') and not k.endswith('.json') and not k.endswith('.ico') and vdomain not in k:
                    h += '<tr><td>' + str(i) + '</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                    i += 1
                if i > 10:
                    break
            h += '</table></p></div></div>' + "\n"
        h += '</div>' + "\n"   # end of row

        # Webstatistics for the last years.
        yth_lbl = []
        yth_usr_desktop = []
        yth_usr_mobile = []
        yth_usr_tablet = []
        yth_usr_bots = []
        yth_usr_visits = []
        prevYear = 9999

        # loop through all dates beginning with highest date:
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            curYear = k[0:4]
            if curYear != prevYear:
                prevYear = curYear
                yth_lbl.append(curYear)
                yth_usr_desktop.append(0)
                yth_usr_mobile.append(0)
                yth_usr_tablet.append(0)
                yth_usr_bots.append(0)
                yth_usr_visits.append(0)
                    
            if 'desktop' in d['v0001']['days'][k]['user']['deviceHits']:
                yth_usr_desktop[-1] += d['v0001']['days'][k]['user']['deviceHits']['desktop']
            if 'mobile' in d['v0001']['days'][k]['user']['deviceHits']:
                yth_usr_mobile[-1] += d['v0001']['days'][k]['user']['deviceHits']['mobile']
            if 'tablet' in d['v0001']['days'][k]['user']['deviceHits']:
                yth_usr_tablet[-1] += d['v0001']['days'][k]['user']['deviceHits']['tablet']
            if 'robot' in d['v0001']['days'][k]['user']['deviceHits']:
                yth_usr_bots[-1] += d['v0001']['days'][k]['user']['deviceHits']['robot']

            # visits:
            if 'visits' in d['v0001']['days'][k]['user']:
                yth_usr_visits[-1] += d['v0001']['days'][k]['user']['visits']

        ## Chart Years:   
        if len(yth_lbl) > 0:
            yth_lbl.reverse()
            yth_usr_desktop.reverse()
            yth_usr_mobile.reverse()
            yth_usr_tablet.reverse()
            yth_usr_bots.reverse()
            yth_usr_visits.reverse()
            h += '<h2>Webstatistics for the last Years for ' + owndomain + '</h2>'
            h += '<div><canvas id="a9x_ws_years"></canvas></div>'
            h += "<script>" + "\n" + "const yth_ctx = document.getElementById('a9x_ws_years');" + "\n"
            h += "const yctx = new Chart(yth_ctx, {"  + "\n"
            h += "  options: { responsive: true, scales: {x:{ stacked: true}, y:{ stacked: true }, y2: { stacked: false, position: 'right'} }}" + "\n"
            h += " ,plugins: { subtitle: { display: true, text: 'Hits per Device Class as of " + d['timelastrec'][0:8] + "'} }" + "\n"
            h += " ,data: { " + "\n" 
            h += "   datasets: [" + "\n"
            h += "      { type: 'bar', label: 'User - Desktop', data: " + str(yth_usr_desktop)+ ", backgroundColor: '#42c5f5', order: 3}" + "\n"
            h += "     ,{ type: 'bar', label: 'User - Mobile',  data: " + str(yth_usr_mobile) + ", backgroundColor: '#42f5aa', order: 4}" + "\n"
            h += "     ,{ type: 'bar', label: 'User - Tablet', data: " + str(yth_usr_tablet) + ", backgroundColor: '#f5a742', order: 5}" + "\n"
            h += "     ,{ type: 'line',label: 'Robots', data: " + str(yth_usr_bots) + ", yAxisID: 'y2', order: 2}" + "\n"
            h += "     ,{ type: 'line',label: 'User - Visit',  data: " + str(yth_usr_visits) + ",backgroundColor: '#ff0000', borderColor: '#ff0000', tension: 0.1, yAxisID: 'y2', order: 1}" + "\n"
            h += "    ]," + "\n"
            h += "    labels: " + str(yth_lbl) + "\n"
            h += " }," + "\n" + "});" + "\n"
            h += "var xmax = 0; "
            h += "var tmax = 0;" + "\n"
            h += "for (i=0; i<5; i++) {" 
            h += "  tmax = Math.max.apply(null, yctx.data.datasets[i].data); "
            h += "  if (tmax > xmax) {  xmax = tmax; } " 
            h += "}" + "\n"
            h += "yctx.options.scales.y.max = xmax + 5;" + "\n"
            h += "yctx.options.scales.y2.max = xmax + 5;" + "\n"
            h += "yctx.update();" + "\n"
            h += "</script>" + "\n"
            
        # Top 10 Domains on year basis
        tsource = {}
        for y in d['v0001']['days']:
            if 'externalFriendsHits' in d['v0001']['days'][y]['user']:
                for sk,sv in d['v0001']['days'][y]['user']['externalFriendsHits'].items():
                    if sk not in tsource:
                        tsource[sk] = 0
                    tsource[sk] += sv['cnt']

        h += '<div class="card text-bg-info mt-2">'
        h += '<div class="card-body">'
        h += '<h3 class="card-title">Top 10 Domains</h3>'
        h += '<h4 class="card-subtitle mb-2 text-body-secondary">Incoming traffic (user hits) for the last years by external source domain</h4>'
        h += '<p class="card-text">'
        h += '<table class="table table-info">'
        h += '<thead><tr><th>Rank</th><th scope="col" style="text-align: left">Domain</th><th scope="col">Hit Count</th></tr></thead>'
        i = 1
        for k, v in sorted(tsource.items(), key=itemgetter(1), reverse=True):
             if owndomain in k:
                 continue
             h += '<tr><td>' + str(i) + '</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
             i += 1
             if i > 10:
                 break
        h += '</table></p></div></div>'  + "\n"

        h += '</div>'
        # End Year
        

        h += '<footer>'
        h += '<a href="https://github.com/ava007/a9x-webstatistics">License and Copyright</a>' + '  V0001'
        h += '<a href="https://www.chartjs.org">Uses chartjs (License)</a>'
        h += '<a href="https://dev.maxmind.com/geoip/geolite2-free-geolocation-data">Uses optionally API to geolite2</a>'
        h += '<pre>URL: Uniform Resource Locator' + "\n"
        h += '<pre>Hit: Download request of a html file' + "\n"
        h += 'salvo errore et omissione'  + "\n"
        h += '</pre>'
        h += '</footer>'

        h += '</div>'  # end of class "container"
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

    runGenCockpitV0001(infile=args.infile, outfile=args.outfile, domain=args.domain)

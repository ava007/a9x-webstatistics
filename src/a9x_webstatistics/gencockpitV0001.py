# -*- coding: utf-8 -*-
import io, ipaddress, sys, argparse, json, ast
from operator import itemgetter
from copy import deepcopy
from importlib.metadata import version
from datetime import datetime, timedelta
from a9x_webstatistics import __version__
from .gencockpitsubV0001 import *
    
def runGenCockpitV0001(infile, outfile, domain, omit, efeature):

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
        tsource = {}
        tcountries = {}
        try:
            for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
                # consider only days:
                if len(k) < 8:
                    continue
                # show at max 31 days:
                if day_usr_i >= 31:
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

                # top 10 source domains:
                if 'externalFriendsHits' in d['v0001']['days'][k]['user']:
                    for sk,sv in d['v0001']['days'][k]['user']['externalFriendsHits'].items():
                        if sk in omit:
                            continue
                        if sk not in tsource:
                            tsource[sk] = 0
                        tsource[sk] += sv['cnt']
                        
                # top 10 countries:
                if 'countryHits' in d['v0001']['days'][k]['user']:
                    for co,cv in d['v0001']['days'][k]['user']['countryHits'].items():
                        if co not in tcountries:
                            tcountries[co] = 0
                        tcountries[co] += cv
  
        except KeyError:
            print('KeyError occured! ' + str(d['v0001']['days'][k]) )
            raise

        day_lbl.reverse()
        day_usr_desktop.reverse()
        day_usr_mobile.reverse()
        day_usr_tablet.reverse()
        day_robot_hits.reverse()
        day_usr_visits.reverse()

        # order for bars:  smallest traffic is "order 1"
        order_mobile = 1
        order_tablet = 2
        order_desktop = 3
        # swap orders if needed:
        if sum(day_usr_tablet) < sum(day_usr_mobile):
            order_tablet, order_mobile = order_mobile, order_tablet
        if sum(day_usr_desktop) < sum(day_usr_tablet):
            order_tablet, order_desktop = order_desktop, order_tablet
        
        h = genHeader(owndomain)
        h += "\n" + '<div class="row pt-3"><div class="col-12">'
        h += '<h1>Webstatistics for ' + owndomain + '</h1>'
        h += '<a href="#hdDay" class="btn btn-primary me-3" role="button" data-bs-toggle="button">Daily Statistics</a>'
        h += '<a href="#hdMonth" class="btn btn-primary me-3" role="button" data-bs-toggle="button">Monthly Statistics</a>'
        h += '<a href="#hdYear" class="btn btn-primary" role="button" data-bs-toggle="button">Yearly Statistics</a>'
        h += '</div></div>'
        h += "\n" + '<div class="row pt-3"><div class="col-12">'
        h += '<h2 id="hdDay">Daily statistics for ' + owndomain + '</h2>'
        h += "<p><small>Last record included in statistic: <script>document.write(DT2Locale('" + d['timelastrec'] + "'));</script></small></p>"
        h += '</div></div>'
        h += "\n" + '<div class="row"><div class="col-12">'
        h += '<h3>Hits and Visits for the last 31 days</h3>'
        h += '<div><canvas id="myChart"></canvas></div>'
        h += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
        h += '<script>' + "\n" + 'const ctx = document.getElementById(\'myChart\');'
        h += "const dctx = new Chart(ctx, {"
        h += " type: 'bar', "  
        h += " options: { responsive: true, scales: {"
        h += "   x: { stacked: true }, "
        h += "   y: { beginAtZero: true, type: 'logarithmic' }"
        h += "  } }"
        h += " ,plugins: { subtitle: { display: true, text: 'Hits per Device Class as of ' + DT2Locale('" + d['timelastrec'] + "') } }"
        h += " ,data: { datasets: [" 
        h += "     { type: 'line',label: 'Robot Hits', data: " + str(day_robot_hits) + "}" + "\n"
        h += "    ,{ type: 'line',label: 'User Visits', data: " + str(day_usr_visits)  + " ,backgroundColor: '#ff0000', borderColor: '#ff0000', tension: 0.1}" + "\n"
        h += "    ,{ type: 'bar', label: 'User Desktop Hits', data: " + str(day_usr_desktop) + ", stack: 's1', backgroundColor: '#42c5f5', order:" + str(order_desktop) + "}" + "\n"
        h += "    ,{ type: 'bar', label: 'User Mobile Hits',  data: " + str(day_usr_mobile) + ", stack: 's1', backgroundColor: '#42f5aa', order:" + str(order_mobile) + "}" + "\n"
        h += "    ,{ type: 'bar', label: 'User Tablet Hits', data: " + str(day_usr_tablet) + ", stack: 's1', backgroundColor: '#f5a742', order:" + str(order_tablet) + "}" + "\n"
        h += "    ],"
        h += "    labels: " + str(day_lbl)
        h += " }," + "\n" + "});"
        h += "var ymax = 0; "
        h += "var ymin = 99999;"
        h += "for (i=0; i<5; i++) {" 
        h += "  var tmax = Math.max.apply(null, dctx.data.datasets[i].data); "
        h += "  if (tmax > ymax) {  ymax = tmax; } " 
        h += "  var tmin = Math.min.apply(null, dctx.data.datasets[i].data); "
        h += "  if (tmin < ymin) {  ymin = tmin; } " 
        h += "}" + "\n"
        h += "rm = ymax % 10;"
        h += "rm = 10 - rm + 10;"
        h += "dctx.options.scales.y.max = ymax + rm;"
        h += "dctx.options.scales.y.min = ymin;"
        h += "dctx.update();"
        h += '</script>'
        h += '</div></div>' + "\n\n"  # end of col and row
        
        lastDate = list(d['v0001']['days'].keys())[-1]
        actYearMonth = lastDate[0:6]
        
        # Top 10 Domains on daily basis
        h += '<div class="row pt-3"><div class="col-md-12 col-lg-6 col-xxl-6">'
        h += '<div class="card mt-2"><div class="card-body">'
        h += '<h3 class="card-title">Top 10 Domains for the last ' + str(day_usr_i) + ' days</h3>'
        h += '<p class="card-text">User hits refering to external domain:</p>'
        h += '<table class="table">'
        h += '<thead><tr><th scope="col" style="text-align: left">Rank</th><th scope="col" style="text-align: left">Domain</th><th scope="col" style="text-align: right">Hit Count</th></tr></thead>'
        i = 1
        for k, v in sorted(tsource.items(), key=itemgetter(1), reverse=True):
             if owndomain in k:
                 continue
             # prevent IP or domains with special characters:
             if any( x in k for x in {'[', ']', ':'} ):
                 continue
             if is_valid_ip(k) == True:  # to suppress ip; ip is not a domain anyway    
                 continue
             h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
             i += 1
             if i > 10:
                 break
        h += '</table>'
        h += '</div></div></div>'  + "\n"   # end of col and card

        # Top Countries
        if len(tcountries) > 0:
            h += '<div class="col-md-12 col-lg-6 col-xxl-6">'
            h += '<div class="card mt-2"><div class="card-body">'
            h += '<h3 class="card-title">Top 10 Countries for the last ' + str(day_usr_i) + ' days</h3>'
            h += '<p class="card-text">User hits by country for the last ' + str(day_usr_i) + ' days:</p>'
            h += '<table class="table">'
            h += '<thead><tr><th>Rank</th><th scope="col" style="text-align: left">Country</th><th scope="col" style="text-align: right">Hit Count</th></tr></thead>'
            i = 1
            for k, v in sorted(tcountries.items(), key=itemgetter(1), reverse=True):
                h += '<tr><td>' +str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                i += 1
                if i > 10:
                    break
            h += '</table>'
            h += '</div></div></div>'    # end of card and col 

        # top urls for the last 31 days:
        ttopurl = {}
        topurlcnt = 0
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            # dont take months in account:
            if len(k) <= 6:
                continue
            if any(oelm in k for oelm in omit):  # don not show parts of url 
                continue
            if topurlcnt >= 31:
                break
            topurlcnt += 1
            if 'topUrl' in d['v0001']['days'][k]['user']:
                for tk, tv in d['v0001']['days'][k]['user']['topUrl'].items():
                    # check if url is blocked for display:
                    if any(oelm in tk for oelm in omit):  # don not show parts of url 
                        continue
                    if tk not in ttopurl:
                        ttopurl[tk] = 0
                    ttopurl[tk] += tv
        if len(ttopurl) > 0:
            h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
            h += '<div class="card mt-2"><div class="card-body">'
            h += '<h3 class="card-title">Top 10 URL</h3>'
            h += '<p class="card-text">User hits for the last ' + str(topurlcnt) + ' days by internal URL on ' + owndomain + ':'
            h += '<table class="table">'
            h += '<thead><tr><th scope="col" style="text-align: left">Rank</th><th scope="col" style="text-align: left">URL</th><th scope="col" style="text-align: right">Hit Count</th></tr></thead>'
            i = 1
            for k, v in sorted(ttopurl.items(), key=itemgetter(1), reverse=True):
                if not k.endswith('.css') and not k.endswith('.json') and not k.endswith('.ico'):
                    h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                    i += 1
                if i > 10:
                    break
            h += '</table>'
            h += '</div></div></div>'   # end of card and col

        # accepted language by browser:
        h += cockpitLanguages(d, owndomain)
        
        # cache, response_time:
        h += performance(d)
       
        # top external landings (friends):
        h += externalFriends(d, owndomain, omit)

        tquality = {}   # nested dictionary!
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            curYearMonth = k[0:6]
            if curYearMonth == actYearMonth:
                if 'quality' in d['v0001']['days'][k]:
                    for sk,sv in d['v0001']['days'][k]['quality'].items():
                        #print('sk: ' + str(sk) + ' sv: ' + str(sv))
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
            h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
            h += '<div class="card mt-2"><div class="card-body">'
            h += '<h3 class="card-title">Quality Improvements</h3>'
            h += '<p class="card-text">Quality improvements that should be implemented:</p>'
            h += '<table class="table-responsive text-break"><thead><tr><th scope="col">Status</th><th scope="col">affected URL</th><th scope="col">Count</th><th scope="col">Remark</th><th scope="col">Date last occured</th></tr></thead>'
            i = 0
            for k, v in sorted(tquality.items(), key=lambda x: (x[1]['lastoccured']), reverse=True):
                h += '<tr><td>' + str(v['status']) + '</td><td>' + str(k) + "</td>" 
                h += '<td style="text-align: right">' + str(format(v['count'],',')) + '</td>'
                h += '<td>' + v['comment'] + '</td>'
                h += "<td><script>document.write(DT2Locale('" + v['lastoccured'] + "'));</script></td>"
                h += '</tr>'
                if len(v['from']) > 1:
                    h += '<tr><td></td><td colspan="4">called by: ' + v['from'] + '</td></tr>'
                i += 1
                if i == 10:
                    break
            h += '</table>'
            h += '</div></div></div>'   # end of card and col
        
        h += '</div>' + "\n\n"   # end of row

        # Navigation for the last 31 days:
        topnav = {}   # nested dictionary!
        days = 0
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            if len(k) < 8:   # not a day anymore
                break
            if 'user' in d['v0001']['days'][k] and 'navigation' in d['v0001']['days'][k]['user']:
                for sk,sv in d['v0001']['days'][k]['user']['navigation'].items():
                    if sk not in topnav:
                        topnav[sk]= sv
                    else:
                        topnav[sk] += sv
            days += 1
            if days > 31:
                break
                            
        if len(topnav) > 1:
            h += '<div class="row pt-3"><div class="col-md-12 col-lg-12 col-xxl-12">'
            h += '<div class="card mt-2"><div class="card-body">'
            h += '<h3 class="card-title">Navigation Analysis for ' + owndomain + '</h3>'
            h += '<p class="card-text">User navigation or flows on internal links:</p>'

            h += '<div id="navpath">'
            h += '<div id="npath" class="vh-100"></div>'
            h += '<script>'
            h += 'var container = document.getElementById("npath");'
            h += 'var dot = "dinetwork { node[shape=box]; '
        
            # loop through path beginning with the most traffic:
            pcount = 0
            navNodes = []
            # setup root:  map(lambda...) for eliminating special characters
            h += "".join(map(lambda char: char if char.isalnum()  else "", owndomain) )  + '[ fontcolor=white, color=red, URL=\\"' + domain + '\\"];'
            
            for pk, pv in sorted(topnav.items(), key=itemgetter(1), reverse=True):
               if any(oelm in pk for oelm in omit):  # don not show parts of url 
                   continue

               if '?' in pk:   # skip wrong data
                   continue
               n = pk.split('(())') 
               if n[0] == n[1]:
                   continue
               # allow only a-z and 0-9:
               if n[0] == '/':    # to avoid empty na
                  n[0] = owndomain
               if n[1] == '/':    # to avoid empty nb
                  n[1] = owndomain
               na = "".join(map(lambda char: char if char.isalnum()  else "", n[0]) )
               nb = "".join(map(lambda char: char if char.isalnum()  else "", n[1]) )
               if len(na) == 0:
                   na = 'root'
               if len(nb) == 0:
                   nb = 'root'
               h += na + ' -> ' + nb 
               if pcount < 5:
                   h += ' [penwidth=4,title=\\"Clicks: ' + str(pv) + '\\"]' 
               elif pcount >= 5 and pcount < 10:
                   h += ' [penwidth=2,title=\\"Clicks: ' + str(pv) + '\\"]' 
               else:
                   h += ' [title=\\"Clicks: ' + str(pv) + '\\"]' 
               # [ label=" ",color="blue",arrowhead="dot" ];
               h += ';'
                         
               # add nodes with their links:
               if n[0] not in navNodes:
                   navNodes.append(n[0])
                   h += na + '[label=\\"' + n[0] + '\\"];'
               if n[1] not in navNodes:
                   navNodes.append(n[1])
                   h += nb + '[label=\\"' + n[1] + '\\"];'
                   
               pcount += 1
               if pcount > 20:
                   break
            h += '}";'
            h += 'var data = vis.parseDOTNetwork(dot);'
            h += 'var network = new vis.Network(container, data);'
            h += '</script>'
            h += '</div>'   # end of navpath

            h += '</div></div>'   # end of card
            h += '</div></div>' + "\n\n"   # end of row

        # navigation chart
        h += navchart(d, owndomain, omit)

        # navigation chart as sankey diagram (experimental feature)
        if efeature == '10':
            h += navchartsankey(d, owndomain, omit)
        
        # Webstatistics for the last months
        tlr = datetime.strptime(d['timelastrec'] + " +0000","%Y%m%d%H%M%S %z")
        tlr_first = tlr.replace(day=1)
        tlr_last_month = tlr_first - timedelta(days=1)
        #print("webstats last months; last is month: " + tlr_last_month.strftime("%Y%m"))

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
                if 'robotHits' in d['v0001']['days'][k]['robot']:
                    mth_usr_bots[-1] += d['v0001']['days'][k]['robot']['robotHits']

                # visits:
                if 'visits' in d['v0001']['days'][k]['user']:
                    mth_usr_visits[-1] += d['v0001']['days'][k]['user']['visits']
               
        ## Months:  
        if len(mth_lbl) > 0:
            h += '<div class="row mt-4"><div class="col-12">'
            mth_lbl.reverse()
            mth_usr_desktop.reverse()
            mth_usr_mobile.reverse()
            mth_usr_tablet.reverse()
            mth_usr_bots.reverse()
            mth_usr_visits.reverse()

            # order for monthly bars:  smallest traffic is "order 1"
            order_mobile = 1
            order_tablet = 2
            order_desktop = 3
            # swap orders if needed:
            if sum(mth_usr_tablet) < sum(mth_usr_mobile):
                order_tablet, order_mobile = order_mobile, order_tablet
            if sum(mth_usr_desktop) < sum(mth_usr_tablet):
                order_tablet, order_desktop = order_desktop, order_tablet
            
            h += '<h2 id="hdMonth">Monthly statistics for ' + owndomain + '</h2>'
            h += '<div><canvas id="a9x_ws_months"></canvas></div>'
            h += "<script>" + "\n" + "const mth_ctx = document.getElementById('a9x_ws_months');" + "\n"
            h += "const mctx = new Chart(mth_ctx, { type: 'bar', " 
            h += "  options: { responsive: true, scales: {"
            h += "     x:{ stacked: true }, "
            h += "     y:{ stacked: true, beginAtZero: true, type: 'logarithmic' }"
            h += "  }}" + "\n"
            h += " ,plugins: { subtitle: { display: true, text: 'Hits per Device Class as of " + d['timelastrec'][0:8]+ " " + d['timelastrec'][-6:] + "'} }" + "\n"
            h += " ,data: { " + "\n" 
            h += "   datasets: [" + "\n"
            h += "      { type: 'bar', label: 'User Desktop Hits',data: " + str(mth_usr_desktop)+ ", stack: 's2', backgroundColor: '#42c5f5', order: " + str(order_desktop) + "}" + "\n"
            h += "     ,{ type: 'bar', label: 'User Mobile Hits', data: " + str(mth_usr_mobile) + ", stack: 's2', backgroundColor: '#42f5aa', order: " + str(order_mobile) + "}" + "\n"
            h += "     ,{ type: 'bar', label: 'User Tablet Hits', data: " + str(mth_usr_tablet) + ", stack: 's2', backgroundColor: '#f5a742', order: " + str(order_tablet) + "}" + "\n"
            h += "     ,{ type: 'line',label: 'Robot Hits', data: " + str(mth_usr_bots) + ", order: 2}" + "\n"
            h += "     ,{ type: 'line',label: 'User Visits',  data: " + str(mth_usr_visits) + ",backgroundColor: '#ff0000', borderColor: '#ff0000', tension: 0.1, order: 1}" + "\n"
            h += "    ],"
            h += "    labels: " + str(mth_lbl)
            h += " }," + "\n" + "});"
            h += "var ymax = 0; "
            h += "var ymin = 999999;"
            h += "for (i=0; i<5; i++) {" 
            h += "  var tmax = Math.max.apply(null, mctx.data.datasets[i].data); "
            h += "  if (tmax > ymax) {  ymax = tmax; } " 
            h += "  var tmin = Math.min.apply(null, mctx.data.datasets[i].data); "
            h += "  if (tmin < ymin) {  ymin = tmin; } " 
            h += "}"
            h += "rm = ymax % 100;"
            h += "rm = 100 - rm + 100;"
            h += "mctx.options.scales.y.max = ymax + rm;"
            h += "mctx.options.scales.y.min = ymin;"
            h += "mctx.update();"
            h += "</script>"
            h += '</div></div>' + "\n\n"  # end of col and row

            # Top 10 Domains on monthly basis
            tsource = {}
            for y in d['v0001']['days']:
                curYearMonth = y[0:6]
                if 'externalFriendsHits' in d['v0001']['days'][y]['user']:
                    for sk,sv in d['v0001']['days'][y]['user']['externalFriendsHits'].items():
                        # prevent IP or domains with special characters:
                        if any( x in sk for x in {'[', ']', ':'} ):
                            continue
                        if is_valid_ip(sk) == True:  # to suppress ip; ip is not a domain anyway    
                            continue
                        if sk not in tsource:
                            tsource[sk] = 0
                        tsource[sk] += sv['cnt']
            h += '<div class="row"><div class="col-md-12 col-lg-6 col-xxl-4">'
            h += '<div class="card mt-2"><div class="card-body">'
            h += '<h3 class="card-title">Top 10 Domains</h3>'
            h += '<p class="card-text">Hit list of domains where traffic comes from:</p>'
            h += '<table class="table">'
            h += '<thead><tr><th scope="col">Rank</th><th scope="col">Domain</th><th scope="col" style="text-align: right">Hit Count</th></tr></thead>'
            i = 1
            for k, v in sorted(tsource.items(), key=itemgetter(1), reverse=True):
                if owndomain in k:
                    continue
                h += '<tr><td>' +str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                i += 1
                if i > 10:
                    break
            h += '</table></div></div></div>'
        
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
                h += '<div class="col-md-12 col-lg-6 col-xxl-4"><div class="card mt-2"><div class="card-body">'
                h += '<h3 class="card-title">Top 10 Countries</h3>'
                h += '<p class="card-text">Hit list of countries giving the most user hits:</p>'
                h += '<table class="table">'
                h += '<thead><tr><th scope="col">Rank</th><th scope="col">Country</th><th scope="col" style="text-align: right">Hits count</th></tr></thead>'
                i = 1
                for k, v in sorted(tcountries.items(), key=itemgetter(1), reverse=True):
                    h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                    i += 1
                    if i == 10:
                        break
                h += '</table></div></div></div>'

            # top urls
            ttopurl = {}
            topurlcnt = 0
            for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
                if len(k) == 6:
                    # check if url is blocked for display:
                    if any(oelm in k for oelm in omit):  # suppress omitted paths 
                        continue

                    if k.endswith('.css') or k.endswith('.json') or k.endswith('.ico') or owndomain in k:
                        continue
                    
                    if topurlcnt > 12:
                        break
                    topurlcnt += 1
                    if 'topUrl' in d['v0001']['days'][k]['user']:
                        for tk, tv in d['v0001']['days'][k]['user']['topUrl'].items():
                            if tk not in ttopurl:
                                ttopurl[tk] = 0
                            ttopurl[tk] += tv
            if len(ttopurl) > 0:
                h += '<div class="col-md-12 col-lg-6 col-xxl-4"><div class="card mt-2"><div class="card-body">'
                h += '<h3 class="card-title">Top 10 URL</h3>'
                h += '<p class="card-text">URL with the most user hits:</p>'
                h += '<table class="table">'
                h += '<thead><tr><th scope="col">Rank</th><th scope="col">URL</th><th scope="col" style="text-align: right">Hit Count</th></tr></thead>'
                i = 1
                for k, v in sorted(ttopurl.items(), key=itemgetter(1), reverse=True):
                    h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                    i += 1
                    if i > 10:
                        break
                h += '</table></div></div></div>' + "\n"   # end of card and col
            h += '</div>' + "\n\n"   # end of row
        # End of Months
        
        
  
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
            if 'robotHits' in d['v0001']['days'][k]['robot']:
                yth_usr_bots[-1] += d['v0001']['days'][k]['robot']['robotHits']

            # visits:
            if 'visits' in d['v0001']['days'][k]['user']:
                yth_usr_visits[-1] += d['v0001']['days'][k]['user']['visits']

        # order for yeary bars:  smallest traffic is "order 1"
        order_mobile = 1
        order_tablet = 2
        order_desktop = 3
        # swap orders if needed:
        if sum(yth_usr_tablet) < sum(yth_usr_mobile):
            order_tablet, order_mobile = order_mobile, order_tablet
        if sum(yth_usr_desktop) < sum(yth_usr_tablet):
            order_tablet, order_desktop = order_desktop, order_tablet

        ## Chart Years:  
        h += '<div class="row mt-4"><div class="col-12">'
        if len(yth_lbl) > 0:
            yth_lbl.reverse()
            yth_usr_desktop.reverse()
            yth_usr_mobile.reverse()
            yth_usr_tablet.reverse()
            yth_usr_bots.reverse()
            yth_usr_visits.reverse()
            h += '<h2 id="hdYear">Yearly statistics for ' + owndomain + '</h2>'
            h += '<div><canvas id="a9x_ws_years"></canvas></div>'
            h += "<script>" + "\n" + "const yth_ctx = document.getElementById('a9x_ws_years');" + "\n"
            h += "const yctx = new Chart(yth_ctx, { type: 'bar',"
            h += "  options: { responsive: true, scales: {x: { stacked: true}, y:{ stacked: true, type: 'logarithmic', beginAtZero: true, min: 0}  }}" + "\n"
            h += " ,plugins: { subtitle: { display: true, text: 'Hits per Device Class as of " + d['timelastrec'][0:8] + "'} }" + "\n"
            h += " ,data: { " + "\n" 
            h += "   datasets: [" + "\n"
            h += "      { type: 'bar', label: 'User Desktop Hits',data: " + str(yth_usr_desktop)+ ", stack: 's3', backgroundColor: '#42c5f5', order: " + str(order_desktop) + "}" + "\n"
            h += "     ,{ type: 'bar', label: 'User Mobile Hits', data: " + str(yth_usr_mobile) + ", stack: 's3', backgroundColor: '#42f5aa', order: " + str(order_mobile) + "}" + "\n"
            h += "     ,{ type: 'bar', label: 'User Tablet Hits', data: " + str(yth_usr_tablet) + ", stack: 's3', backgroundColor: '#f5a742', order: " + str(order_tablet) + "}" + "\n"
            h += "     ,{ type: 'line',label: 'Robot Hits', data: " + str(yth_usr_bots) + ", order: 2}" + "\n"
            h += "     ,{ type: 'line',label: 'User Visits',  data: " + str(yth_usr_visits) + ",backgroundColor: '#ff0000', borderColor: '#ff0000', tension: 0.1, order: 1}" + "\n"
            h += "    ]," + "\n"
            h += "    labels: " + str(yth_lbl) + "\n"
            h += " }," + "\n" + "});" + "\n"
            h += "var ymax = 0; "
            h += "var ymin = 99999;" + "\n"
            h += "for (i=0; i<5; i++) {" 
            h += "  var tmax = Math.max.apply(null, yctx.data.datasets[i].data); "
            h += "  if (tmax > ymax) {  ymax = tmax; } " 
            h += "  var tmin = Math.min.apply(null, yctx.data.datasets[i].data); "
            h += "  if (tmin < ymin) {  ymin = tmin; } " 
            h += "}"
            h += "rm = ymax % 1000;"
            h += "rm = 1000 - rm + 1000;"
            h += "yctx.options.scales.y.max = ymax + rm;"
            h += "yctx.options.scales.y.min = ymin;"
            h += "yctx.update();"
            h += "</script>" + "\n"

        h += '</div></div>' + "\n\n"   # End of Row
            
        # Top 10 Domains on year basis
        tsource = {}
        for y in d['v0001']['days']:
            if 'externalFriendsHits' in d['v0001']['days'][y]['user']:
                for sk,sv in d['v0001']['days'][y]['user']['externalFriendsHits'].items():
                    # prevent IP or domains with special characters:
                    if any( x in sk for x in {'[', ']', ':'} ):
                        continue
                    if is_valid_ip(sk) == True:  # to suppress ip; ip is not a domain anyway    
                        continue
                    if sk not in tsource:
                        tsource[sk] = 0
                    tsource[sk] += sv['cnt']

        h += '<div class="row mt-4"><div class="col-md-12 col-lg-6 col-xxl-4"><div class="card mt-2"><div class="card-body">'
        h += '<h3 class="card-title">Top 10 Domains</h3>'
        h += '<p class="card-text">Incoming traffic (user hits) for the last years by external source domain:</p>'
        h += '<table class="table">'
        h += '<thead><tr><th>Rank</th><th scope="col" style="text-align: left">Domain</th><th scope="col" style="text-align: right">Hit Count</th></tr></thead>'
        i = 1
        for k, v in sorted(tsource.items(), key=itemgetter(1), reverse=True):
             if owndomain in k:
                 continue
             h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
             i += 1
             if i > 10:
                 break
        h += '</table></div></div></div>'

        # Top 10 URL on year basis
        turl = {}
        for y in d['v0001']['days']:
            if 'topUrl' in d['v0001']['days'][y]['user']:
                for sk,sv in d['v0001']['days'][y]['user']['topUrl'].items():
                    # check if url is blocked for display:
                    if any(oelm in sk for oelm in omit):  # suppress omitted paths 
                        continue
                    if sk not in turl:
                        turl[sk] = 0
                    turl[sk] += sv

        h += '<div class="col-md-12 col-lg-6 col-xxl-4"><div class="card mt-2"><div class="card-body">'
        h += '<h3 class="card-title">Top 10 URL</h3>'
        h += '<p class="card-text">Top Url (user hits) for the last years:</p>'
        h += '<table class="table">'
        h += '<thead><tr><th>Rank</th><th scope="col" style="text-align: left">URL</th><th scope="col" style="text-align: right">Hit Count</th></tr></thead>'
        i = 1
        for k, v in sorted(turl.items(), key=itemgetter(1), reverse=True):
             if owndomain in k:
                 continue
             h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
             i += 1
             if i > 10:
                 break
        h += '</table></div></div></div>'
        h += '</div>'  + "\n\n"   # end of row
        
        # End Year

        h += '<footer class="row bg-light py-4 mt-4">'

        h += '<div class="col"><h2>About</h2>'
        h += '<ul class="nav flex-column">'
        h += '<li class="nav-item mb-2"><a href="https://github.com/ava007/a9x-webstatistics" class="nav-link p-0 text-body-secondary">© 2024-2025 a9x-webstatistics</a></li>'
        h += '<li class="nav-item mb-2">' + __version__ + '</li>'
        h += '<li class="nav-item mb-2">salvo errore et omissione</li>'
        h += '</ul></div>' + "\n"

        h += '<div class="col"><h2>Powered by</h2>'
        h += '<ul class="nav flex-column">'
        h += '<li class="nav-item mb-2"><a href="https://www.logikfabrik.com" class="nav-link p-0 text-body-secondary">LogikFabrik.com</a></li>'
        h += '<li class="nav-item mb-2"><a href="https://www.logikfabrik.com/webstatsLF24.html" class="nav-link p-0 text-body-secondary">Live Example</a></li>'
        h += '</ul></div>' + "\n"
          
        h += '<div class="col"><h2>Abbreviations</h2>'
        h += '<ul class="nav flex-column">'
        h += '<li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">Hit: Download request of a html file</a></li>'
        h += '<li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">URL: Uniform Resource Locator</a></li>'
        h += '</ul></div>' + "\n"

        h += '</footer>'

        h += '</div>'  # end of class "container"
        h += '</body></html>'

        # write html to file:
        outfile = open(outfile, "w")
        outfile.write(h)
        outfile.close()

        return 0
        
def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False,
        prog='a9x_webstatistics',
        epilog="Version: "+ version('a9x-webstatistics')
    )
    parser.add_argument("-i", "--infile", help="json file that contains calculated statistics", default="webstat.json")
    parser.add_argument("-o", "--outfile", help="html file that contains html cockpit", default="webstat.html")
    parser.add_argument("-d", "--domain", help="domain https://logikfabrik.com on which the access log file runs", default="https://logikfabrik.com")
    parser.add_argument("-t", "--omit", help="omits path ie. will not display these path in generated cockpit", action="append")
    args, unknown = parser.parse_known_args()

    if args.omit is None:
        args.omit = []        

    runGenCockpitV0001(infile=args.infile, outfile=args.outfile, domain=args.domain, omit=args.omit)

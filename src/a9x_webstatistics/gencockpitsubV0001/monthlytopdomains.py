# -*- coding: utf-8 -*-
from operator import itemgetter
from datetime import datetime, timedelta
from .validip import is_valid_ip

def monthlyTopDomains(d, owndomain, omit):
    
    # calc month preceeding to timelastrec:
    tlr = datetime.strptime(d['timelastrec'] + " +0000","%Y%m%d%H%M%S %z")
    tlr_first_day_of_month = tlr.replace(day=1)
    tlr_last_period = tlr_first_day_of_month - timedelta(days=1)
    maxPeriodYM = tlr_last_period.strftime("%Y%m")
    
    cnt = 0
    startPeriod = None
    endPeriod = None
    tsource = {}
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        curPeriodYM = k[0:6]

        # skip current month data
        if len(curPeriodYM) == 6 and curPeriodYM > maxPeriodYM:
            continue
 
        # top 10 source domains:
        if 'nav' in d['v0001']['days'][k]['user']:
            # sort by count e['c'] desc:
            for e in sorted(d['v0001']['days'][k]['user']['nav'], key=lambda x: x['c'], reverse=True):
                if 'p' not in e or 'e' not in e['p']:   # internal links
                    continue
                if e['s'] in omit:
                    continue
                if e['t'] in omit:
                    continue
                if e['s'] not in tsource:
                    if len(tsource) > 80:
                        continue
                    tsource[e['s']] = 0
       
                tsource[e['s']] += e['c']
                
                # record start / end period to be displayed on chart:
                if startPeriod is None or curPeriodYM < startPeriod:
                    startPeriod = curPeriodYM
                if endPeriod is None:
                    endPeriod = curPeriodYM
    
    if len(tsource) == 0:
        return ''
    
    # Top 10 Domains on daily basis
    # row needs to be decleared in the calling function h+= '<div class="row pt-3">'
    h = "\n" + '<div class="col-md-12 col-lg-6 col-xxl-6">'
    h += '<h3>Top 10 Domains - Long Term</h3>'
    h += '<p>User hits refering to external domains from ' + startPeriod  + ' to ' + endPeriod + ':</p>'
    h += '<table class="table">'
    h += '<thead><tr><th scope="col" style="text-align: left">Rank</th><th scope="col" style="text-align: left">Domain</th><th scope="col" style="text-align: right">Hits</th></tr></thead>'
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
    h += '</div>'  + "\n"   # end of col and card
 
    return h

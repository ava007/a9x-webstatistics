# -*- coding: utf-8 -*-
from operator import itemgetter
from .validip import is_valid_ip

def monthlyTopCountries(d, owndomain, omit):
    tcountries = {}
    tcnt = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # consider only days:
        if len(k) > 6:
            continue
        # show at max 31 days:
        if tcnt >= 31:
            break
        tcnt += 1

        if 'countryHits' in d['v0001']['days'][k]['user']:
            for co,cv in d['v0001']['days'][k]['user']['countryHits'].items():
                if co not in tcountries:
                    tcountries[co] = 0
                tcountries[co] += cv
           
    if len(tcountries) == 0:
        return ''
    
    h = "\n" + '<div class="col-md-12 col-lg-6 col-xxl-6 pt-3">'
    h += '<h3>Top 10 Countries - Long Term</h3>'
    h += '<p>User hits from countries on ' + owndomain + ':'
    h += '<table class="table">'
    h += '<thead><tr><th scope="col" style="text-align: left">Rank</th><th scope="col" style="text-align: left">Country</th><th scope="col" style="text-align: right">Hits</th></tr></thead>'
    i = 1
    for k, v in sorted(tcountries.items(), key=itemgetter(1), reverse=True):
        if not k.endswith('.css') and not k.endswith('.json') and not k.endswith('.ico'):
            h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
            i += 1
            if i > 10:
                break
    h += '</table>'
    h += '</div>'  + "\n"   # end of col and card
 
    return h

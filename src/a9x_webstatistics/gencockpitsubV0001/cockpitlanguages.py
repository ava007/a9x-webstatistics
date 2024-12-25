# -*- coding: utf-8 -*-
import json
from operator import itemgetter

# top languages for the last 31 days:
def cockpitLanguages(d, owndomain):
    
    # accumulate the results for maximum the last 31 days:
    toplng = {}
    toplngcnt = 0
    total_languages = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # dont take months in account:
        if len(k) <= 6:
            continue
        if toplngcnt >= 31:
            break
        toplngcnt += 1
        if 'language' in d['v0001']['days'][k]['user']:
            for tk, tv in d['v0001']['days'][k]['user']['language'].items():
                if tk not in toplng:
                    toplng[tk] = 0
                toplng[tk] += tv
                total_languages += tv
                
    # show results if available:
    h = ''
    if len(toplng) > 0:
        h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
        h += '<div class="card mt-2"><div class="card-body">'
        h += '<h3 class="card-title">Top 10 Languages</h3>'
        h += '<p class="card-text">User languages for the last ' + str(toplngcnt) + ' days by based on user hits  on ' + owndomain + ':'
        h += '<table class="table">'
        h += '<thead>'
        h += '<tr><th scope="col" style="text-align: left">Rank</th><th scope="col" style="text-align: left">Language</th>'
        h += '<th scope="col" style="text-align: right">Hit Count</th><th scope="col" style="text-align: right">Percentage</th></tr>'
        h += '</thead>'
        i = 1
        for k, v in sorted(toplng.items(), key=itemgetter(1), reverse=True):
            h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td>'
            h += '<td style="text-align: right">' + str(format(v, ',')) + '</td>'
            h += '<td style="text-align: right">{:.0%}</td>'.format(v / total_languages)
            h += '</tr>'
            i += 1
            if i > 10:
                break
        h += '</table></p>'
        h += '</div></div></div>'   # end of card and col
    return h

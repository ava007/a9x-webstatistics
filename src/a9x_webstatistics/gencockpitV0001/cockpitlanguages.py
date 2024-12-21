# -*- coding: utf-8 -*-
import json
from operator import itemgetter
    
def cockpitLanguages(d, owndomain):
    # top Languages for the last 31 days:
    h = ''
    toplng = {}
    toplngcnt = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # dont take months in account:
        if len(k) <= 6:
            continue
        if topurlcnt >= 31:
            break
        topurlcnt += 1
        if 'language' in d['v0001']['days'][k]['user']:
            for tk, tv in d['v0001']['days'][k]['user']['language'].items():
                if tk not in ttopurl:
                    toplng[tk] = 0
                toplng[tk] += tv
        if len(toplng) > 0:
            h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
            h += '<div class="card mt-2"><div class="card-body">'
            h += '<h3 class="card-title">Top 10 Languages</h3>'
            h += '<p class="card-text">User Languages for the last ' + str(toplngcnt) + ' days by internal URL on ' + owndomain + ':'
            h += '<table class="table">'
            h += '<thead><tr><th scope="col" style="text-align: left">Rank</th><th scope="col" style="text-align: left">URL</th><th scope="col" style="text-align: right">Hit Count</th></tr></thead>'
            i = 1
            for k, v in sorted(toplng.items(), key=itemgetter(1), reverse=True):
                h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
                i += 1
                if i > 10:
                    break
            h += '</table>'
            h += '</div></div></div>'   # end of card and col
    return h

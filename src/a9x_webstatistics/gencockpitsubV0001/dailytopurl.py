# -*- coding: utf-8 -*-
from operator import itemgetter
from .validip import is_valid_ip

def dailyTopUrl(d, owndomain, omit):
    topurlcnt = 0
    topurl = {}
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # consider only days:
        if len(k) < 8:
            continue
        if any(oelm in k for oelm in omit):  # don not show parts of url 
            continue
        # show at max 31 days:
        if topurlcnt >= 31:
            break
        topurlcnt += 1

        # top 10 source domains:
        if 'topUrl' in d['v0001']['days'][k]['user']:
            for tk, tv in d['v0001']['days'][k]['user']['topUrl'].items():
                # check if url is blocked for display:
                if any(oelm in tk for oelm in omit):  # don not show parts of url 
                    continue
                if tk not in topurl:
                    topurl[tk] = 0
                topurl[tk] += tv
   
    if len(topurl) == 0:
        return ''
    
    h = "\n" + '<div class="col-md-12 col-lg-6 col-xxl-6">'
    h += '<h3>Top 10 URL</h3>'
    h += '<p>User hits for the last ' + str(topurlcnt) + ' days by internal URL on ' + owndomain + ':'
    h += '<table class="table">'
    h += '<thead><tr><th scope="col" style="text-align: left">Rank</th><th scope="col" style="text-align: left">URL</th><th scope="col" style="text-align: right">Hits</th></tr></thead>'
    i = 1
    for k, v in sorted(topurl.items(), key=itemgetter(1), reverse=True):
        if not k.endswith('.css') and not k.endswith('.json') and not k.endswith('.ico'):
            h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
            i += 1
            if i > 10:
                break
    h += '</table>'
    h += '</div>'  + "\n"   # end of col and card
 
    return h

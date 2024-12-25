# -*- coding: utf-8 -*-
import ipaddress
from operator import itemgetter

# top external landings (friends) for max 31 days:
def externalFriends(d, owndomain, omit):
    tland = {}   # nested dictionary!
    topland = 0
    h = ''
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit months or years:
        if len(k) <= 6:
            continue
        if topland >= 31:
            break
        topland += 1
        if 'externalFriendsHits' in d['v0001']['days'][k]['user']:
            for tk, tv in d['v0001']['days'][k]['user']['externalFriendsHits'].items():
                # check if url is blocked for display:
                if any(oelm in tk for oelm in omit):  # don not show parts of url 
                    continue
                if tk not in tland:
                    tland[tk] = {}
                for tdk,tdv in tv['target'].items():
                    if tdk not in tland[tk]:
                        tland[tk][tdk] = 0
                    tland[tk][tdk] += tdv
                    
    if len(tland) > 0:
        #print("tland: " + str(tland) )
        h += '<div class="col-md-12 col-lg-6 col-xxl-4">'
        h += '<div class="card mt-2"><div class="card-body">'
        h += '<h3 class="card-title">Top 10 Landings</h3>'
        h += '<p class="card-text">User landings for the current month:</p>'
        h += '<table class="table-responsive text-break"><thead>'
        h += '<tr><th scope="col" style="text-align: left">Rank</th><th scope="col">Source</th><th scope="col">Target</th><th scope="col" style="text-align: right">Count</th></tr>'
        h += '</thead>'
        i = 1
        for k, v in sorted(tland.items(), key=itemgetter(0), reverse=True):
            # check if url is blocked for display:
            if any(oelm in k for oelm in omit):  # don not show parts of url 
                 continue
            if is_valid_ip(k) == True:  # to suppress ip; ip is not a domain anyway    
                 continue

            for kb, vb in v.items():
                h += '<tr><td>' + str(i) + '.</td><td>' + k + '</td><td>' + str(kb) + '</td><td style="text-align: right">' + str(vb) + '</td></tr>'
                i += 1
                if i > 10:
                    break

        h += '</table>'
        h += '</div></div></div>'
    return h

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

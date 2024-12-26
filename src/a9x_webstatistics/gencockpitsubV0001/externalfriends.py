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
                if is_valid_ip(tk) == True:  # to suppress ip; ip is not a domain anyway    
                    continue
                if '[' in tk:    # hack for IPv6 addresses
                    continue
                if tk not in tland:
                    tland[tk] = {}
                    tland[tk]['cnt'] = 0
                    tland[tk]['target'] = {}
                for tdk,tdv in tv['target'].items():
                    # check if url is blocked for display:
                    if any(oelm in tdk for oelm in omit):  # don not show parts of url 
                        continue
                    if tdk not in tland[tk]['target']:
                        tland[tk]['target'][tdk] = 0
                    tland[tk]['target'][tdk] += tdv
                    tland[tk]['cnt'] += tdv
                    
    if len(tland) > 0:
        #print("tland: " + str(tland) )
        h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
        h += '<div class="card mt-2"><div class="card-body">'
        h += '<h3 class="card-title">Top 10 Landings</h3>'
        h += '<p class="card-text">User landings from external domains for the current month:</p>'
        h += '<div class="table-responsive">'
        h += '<table class="table text-break table-striped"><thead>'
        h += '<tr><th scope="col" style="text-align: left">Rank</th><th scope="col">Source</th><th scope="col">Count Source</th><th scope="col">Target</th><th scope="col" style="text-align: right">Count Target</th></tr>'
        h += '</thead><tbody>'
        i = 1
        j = 1
        prev_k = ''
        for k, v in sorted(tland.items(), key=lambda x: x[1]['cnt'], reverse=True):
            #print("k/v: " + str(k) + " --> " + str(v))
            for kb, vb in sorted(v['target'].items(), key=lambda item: item[1], reverse=True):
                h += '<tr>'
                if k == prev_k:
                    h += '<td></td><td></td><td></td>'
                else:
                    h += '<td>' + str(i) + '.</td><td>' + k + '</td><td>' + str(v['cnt']) + '</td>'
                    i += 1
                j += 1
                h += '<td>' + str(kb) + '</td><td style="text-align: right">' + str(vb) + '</td>'
                h += '</tr>'
              
                if i > 10 or j > 24:
                    break
                prev_k = k
                       
        h += '</tbody></table></div>'
        h += '</div></div></div>'
    return h

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

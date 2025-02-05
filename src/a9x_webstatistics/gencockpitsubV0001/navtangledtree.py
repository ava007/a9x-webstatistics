# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart:
def navchart_tangledtree(d, owndomain, omit):
    h = ''
    #const levels = [[{'id': 'start'}], [{'id': 'business', 'parents': ['start']}], [{'id': 'comparison', 'parents': ['start']}]
    levels = [[{'id': 'start'}]]
    
    days = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit months or years:
        if len(k) < 8:
            break
        days += 1
        if 'externalFriendsHits' in d['v0001']['days'][k]['user']:
            for tk, tv in d['v0001']['days'][k]['user']['externalFriendsHits'].items():
                if is_valid_ip(tk) == True:  # to suppress ip; ip is not a domain anyway    
                    continue
                if '[' in tk:    # hack for IPv6 addresses
                    continue
                tmp = {}
                tmplink['id'] = tk
                tmplink['parents'] = ['start']
                levels.append(tmplist)
                
                #for tdk,tdv in tv['target'].items():
                #    if any(oelm in tdk for oelm in omit):  # don not show parts of url 
                #        continue
                #    if tdk == '/':
                #        tmplink['target'] = "".join(map(lambda char: char if char.isalnum()  else "", owndomain) ) # eliminate special chars
                #    else:
                #        tmplink['target'] =  "".join(map(lambda char: char if char.isalnum()  else "", tdk) ) # eliminate special chars
                #    duplicate_found = False
                #    for li in links:
                #        if (li['source'] == tmplink['source']
                #                and li['target'] == tmplink['target']):
                #            duplicate_found = True
                #            li['cnt'] += tdv
                #            break
                #    if duplicate_found == False:
                #        links.append(tmplink)

    # d3js horizontal bubble char in case results are available:
    h += "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
    h += '<div class="card mt-2"><div class="card-body">'
    h += '<h3 class="card-title">Navigation Chart</h3>'
    h += '<p class="card-text">User Navigation Chart for ' + owndomain + ':</p>'
    h += '<div id="navchart-tangledtree-container"><svg id="svgchart" width="600" height="400"></svg></div>'
    h += '<script type="module">' + "\n"
    h += 'const levels = ' + str(levels) + ';' + "\n"

    h += 'const rect = document.getElementById("navchart-tangledtree-container").getBoundingClientRect();'
    h += "</script>"

    h += '</div></div></div>'
    return h

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

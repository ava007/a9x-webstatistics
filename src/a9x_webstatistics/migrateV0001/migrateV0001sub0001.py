import json
from copy import deepcopy
from operator import itemgetter

# This function is not yet in operation i.e. being called. It's in preparation!
# Migrations:
# 1. User --> ExternalFriendsHits migrate to User --> Nav   (list of dict)
# 2. User --> Navigation migrate to User --> Nav
#
#     nav:[
#        { 's': 'www.google.com',  # s=source
#          't': '/',   # t=target
#          'c': 1      # count
#          'p': 'e'    # type: e=external, empty: internal
#        },
#     ]
#
#
#  Migrationsteps:
#  a)  Build Chart based on user->Nav with fixed experimental data   ---> Prod (if domain = logikfabrik.com)
#  b)  New Data goes into user->Nav    ---> Beta
#  c)  Migrate using this function    ---> Beta
#  d)  Discard old Navigation         ---> Prod

def migv0001sub0001(
    statfile
    ):
    try:
        f = open(statfile) 
        d = json.load(f) 
    except FileNotFoundError:   # first call: file does not exists
        print("-s statistic file not found, it will be automatically created")
        return
    except json.JSONDecodeError:
        print("-s json file is not valid")
        return

    # save
    tstat = statfile.replace('.json','v0001sub0001before.json')
    with open(tstat, "w") as sf:
       json.dump(d,sf)

    # iterate on days reverse and consolidate nav data on the last day of the month:
    lastDay = ''
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # change of month:
        if lastDay is not None and lastDay[0:6] != k[0:6]:
            lastDay = k
        if lastDay is None:  # inital call
            lastDay = k
        
        if 'user' in d['v0001']['days'][k]:
            if 'externalFriendsHits' in d['v0001']['days'][k]['user']:
                if 'nav' not in d['v0001']['days'][lastDay]['user']:
                    d['v0001']['days'][lastDay]['user']['nav'] = []
                for tk, tv in d['v0001']['days'][k]['user']['externalFriendsHits'].items():
                    print("tk: " + str(tk) + " tv: " + str(tv))
                    for tdk,tdv in tv['target'].items():
                        tmprec = {}
                        tmprec['s'] = tk   # Source
                        tmprec['t'] = tdk  # Target
                        tmprec['p'] = 'e'  # type: e=external source, i=internal source
                        tmprec['c'] = int(tdv)   # count
                        print("tmprec: " + str(tmprec))
                        # check if source and target already exists:
                        #if next(item for item in d['v0001']['days'][x]['user']['nav'] if item['s'] == tmprec['s] and item['t'] == tmprec['t']):
                        for e in d['v0001']['days'][lastDay]['user']['nav']:
                            if e['s'] == tmprec['s']
                                    and e['t'] = tmprec['t']:
                                e['c'] += tmprec['c']
                            else:
                                d['v0001']['days'][lastDay]['user']['nav'].append(tmprec)
                #todo:  delete externalFriendsHits
            if 'navigation' in d['v0001']['days'][k]['user']:
                if 'nav' not in d['v0001']['days'][lastDay]['user']:
                    d['v0001']['days'][lastDay]['user']['nav'] = []
                for nk, nv in d['v0001']['days'][k]['user']['navigation'].items():
                    print("navigation nk: " + str(nk) + " nv: " + str(nv))
                    n = nk.split('(())') 
                    if n[0] == n[1]:
                        continue
                    tmprec = {}
                    tmprec['s'] = n[0]    # Source
                    tmprec['t'] = n[1]    # Target
                    #tmprec['p'] = 'i'     # type: e=external source, i=internal source
                    tmprec['c'] = int(nv) # count
                    for e in d['v0001']['days'][k]['user']['nav']:
                        if e['s'] == tmprec['s']
                                and e['t'] = tmprec['t']:
                            e['c'] += tmprec['c']
                        else:
                            d['v0001']['days'][k]['user']['nav'].append(tmprec)
                #todo:  delete navgation

    # write updated statistic file:
    #with open(statfile, "w") as sf:
    #   json.dump(d,sf)

    return        

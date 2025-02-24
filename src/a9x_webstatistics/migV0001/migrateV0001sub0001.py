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
#  a)  this function works and writes to separate external file
#  a)  Build Chart based on user->Nav with fixed experimental data and experimental feature   ---> Prod (if domain = logikfabrik.com)
#  b)  New Data goes into user->Nav    ---> Beta
#  c)  activate this migration function, write to production file    ---> Beta
#  d)  Discard old Navigation         ---> Prod

def addnav(d, lday, trec):
    found = False
    if (trec['s'] is None 
            or trec['t'] is None):
        return d
    for e in d['v0001']['days'][lday]['user']['nav']:
        if (e['s'] == trec['s']
                and e['t'] == trec['t']):
            e['c'] += trec['c']
            found = True
            break
    if found == False:
        d['v0001']['days'][lday]['user']['nav'].append(trec)

    return d

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

    # make sure that migration runs only once!!!
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0)):
         if 'user' in d['v0001']['days'][k]:
             if 'nav' in d['v0001']['days'][k]['user']:
                 return

    print("v0001sub0001 start migration")
    dtmp = deepcopy(d)
    # save
    tstat = statfile.replace('.json','v0001sub0001before.json')
    with open(tstat, "w") as sf:
       json.dump(d,sf)

    navcount = 0
    # iterate on days reverse and consolidate nav data on the last day of the month:
    lastDay = ''
    for k, v in sorted(dtmp['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # change of month:
        if lastDay is not None and lastDay[0:6] != k[0:6]:
            lastDay = k
        if lastDay is None:  # inital call
            lastDay = k
        
        if 'user' in dtmp['v0001']['days'][k]:
            if 'externalFriendsHits' in dtmp['v0001']['days'][k]['user']:
                if 'nav' not in d['v0001']['days'][lastDay]['user']:
                    d['v0001']['days'][lastDay]['user']['nav'] = []
                for tk, tv in dtmp['v0001']['days'][k]['user']['externalFriendsHits'].items():
                    #print("tk: " + str(tk) + " tv: " + str(tv))
                    for tdk,tdv in tv['target'].items():
                        tmprec = {}
                        tmprec['s'] = tk   # Source
                        tmprec['t'] = tdk  # Target
                        tmprec['p'] = 'e'  # type: e=external source, i=internal source
                        tmprec['c'] = int(tdv)   # count
                        #print("tmprec: " + str(tmprec))
                        d = addnav(d, lastDay, tmprec)
                        navcount += 1
                del d['v0001']['days'][k]['user']['externalFriendsHits']

            if 'navigation' in dtmp['v0001']['days'][k]['user']:
                if 'nav' not in d['v0001']['days'][lastDay]['user']:
                    d['v0001']['days'][lastDay]['user']['nav'] = []
                for nk, nv in dtmp['v0001']['days'][k]['user']['navigation'].items():
                    #print("navigation nk: " + str(nk) + " nv: " + str(nv))
                    n = nk.split('(())') 
                    if n[0] == n[1]:
                        continue
                    tmprec = {}
                    tmprec['s'] = n[0]    # Source
                    tmprec['t'] = n[1]    # Target
                    tmprec['c'] = int(nv) # count
                    d = addnav(d, lastDay, tmprec)
                    navcount += 1
                del d['v0001']['days'][k]['user']['navigation']

    # write updated statistic file:
    with open(statfile, "w") as sf:
       json.dump(d,sf)

    print("v0001sub0001 end migration: " + str(navcount) + " items processed")

    #try:
    #    print("\nmigrateV001sub0001.py 20250223: " + "\n " + str(d['v0001']['days']['20250223']['user']) )
    #except KeyError:
    #    pass   # do nothing

    return        

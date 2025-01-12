import json
from copy import deepcopy

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

    # Migrations:
    # 1. User --> ExternalFriendsHits migrate to User --> Nav   (list of dict)
    # 2. User --> Navigation migrate to User --> Nav

    # save
    tstat = statfile.replace('.json','v0001sub0001before.json')
    with open(tstat, "w") as sf:
       json.dump(d,sf)

    for x in d['days']:
        if 'user' in d['v0001']['days'][x]:
            if 'externalFriendsHits' d['v0001']['days'][x]['user']:
                if 'nav' not in d['v0001']['days'][x]['user']:
                    d['v0001']['days'][x]['user']['nav'] = []
                for tk, tv in d['v0001']['days'][x]['user']['externalFriendsHits'].items():
                    print("tk: " + str(tk) + " tv: " + str(tv))
                    for tdk,tdv in tv['target'].items():
                        tmprec = {}
                        tmprec['s'] = tk   # Source
                        tmprec['t'] = tdk  # Target
                        tmprec['y'] = 'e'  # type: e=external source, i=internal source
                        tmprec['c'] = int(tdv)   # count
                        print("tmprec: " + str(tmprec))
                        # check if source and target already exists:
                        #if next(item for item in d['v0001']['days'][x]['user']['nav'] if item['s'] == tmprec['s] and item['t'] == tmprec['t']):
                        for e in d['v0001']['days'][x]['user']['nav']:
                            if e['s'] == tmprec['s']
                                    and e['t'] = tmprec['t']:
                                e['c'] += tmprec['c']
                            else:
                                d['v0001']['days'][x]['user']['nav'].append(tmprec)
                        #todo:  delete externalFriendsHits
                            
        
        

    # write updated statistic file:
    #with open(statfile, "w") as sf:
    #   json.dump(d,sf)

    return        

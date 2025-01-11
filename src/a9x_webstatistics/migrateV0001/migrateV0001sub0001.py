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

    # loop through extern friendsHits:

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
                    for tdk,tdv in tv['target'].items():
                        tmprec = {}
                        tmprec['s'] = tk   # Source
                        tmprec['t'] = tdk  # Target
                        tmprec['y'] = 'e'  # type: e=external source, i=internal source
                        tmprec['c'] = tdv
                        # check if source and target already exists:
        

    # write updated statistic file:
    #with open(statfile, "w") as sf:
    #   json.dump(d,sf)

    return        

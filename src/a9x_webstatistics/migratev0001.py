import json
def migv0001(
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
        
    # return if already migrated:
    if 'v0001' in d:
        return
    d['v0001'] = {}
    d['v0001']['days'] = {}
    for x in d['days']:
        d['v0001']['days'][x] = {}
        d['v0001']['days'][x]['user'] = {}
        d['v0001']['days'][x]['user']['country_hits'] = d['days'][x]['countries']
        d['v0001']['days'][x]['user']['device_hits'] = {}
        d['v0001']['days'][x]['user']['device_hits']['desktop'] = d['days'][x]['device_hits']['desktop']
        d['v0001']['days'][x]['user']['device_hits']['mobile'] = d['days'][x]['device_hits']['mobile']
        d['v0001']['days'][x]['user']['device_hits']['tablet'] = d['days'][x]['device_hits']['tablet']
        d['v0001']['days'][x]['robot'] = 0
        if 'bots' in d['days'][x]['device_hits']:
            d['v0001']['days'][x]['robot'] += d['days'][x]['device_hits']['bots'] 
        if 'others' in d['days'][x]['device_hits']:
            d['v0001']['days'][x]['robot'] += d['days'][x]['device_hits']['others'] 
        d['v0001']['days'][x]['quality'] = {}

    # write updated statistic file:
    tstat = statfile.replace('.json','v0001.json')
    
    with open(tstat, "w") as sf:
       json.dump(d,sf)
    return

        


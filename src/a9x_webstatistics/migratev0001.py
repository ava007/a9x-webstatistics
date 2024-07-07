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
        d['v0001']['days'][x]['user']['visits'] = 0
        if 'visits' in d['days'][x]:
            d['v0001']['days'][x]['user']['visits'] = d['days'][x]['visits']
            
        d['v0001']['days'][x]['user']['bytes_sent'] = 0
        if 'bytes_sent' in d['days'][x]:
            d['v0001']['days'][x]['user']['bytes_sent'] = d['days'][x]['bytes_sent']
            
        d['v0001']['days'][x]['user']['country_hits'] = d['days'][x]['countries']
        d['v0001']['days'][x]['user']['device_hits'] = {}
        d['v0001']['days'][x]['user']['device_hits']['desktop'] = d['days'][x]['device_hits']['desktop']
        d['v0001']['days'][x]['user']['device_hits']['mobile'] = d['days'][x]['device_hits']['mobile']
        d['v0001']['days'][x]['user']['device_hits']['tablet'] = d['days'][x]['device_hits']['tablet']
        d['v0001']['days'][x]['user']['external_friends_hits'] = {}
        if 'friends' in d['days'][x]:
            d['v0001']['days'][x]['user']['external_friends_hits'] = d['days'][x]['friends']
        d['v0001']['days'][x]['user']['top_url'] = {}
        if 'topurl' in d['days'][x]:
            d['v0001']['days'][x]['user']['top_url'] = d['days'][x]['topurl']

        d['v0001']['days'][x]['robot'] = {}
        d['v0001']['days'][x]['robot']['bytes_sent'] = 0
        d['v0001']['days'][x]['robot']['robot_hits'] = 0
        if 'bots' in d['days'][x]['device_hits']:
            d['v0001']['days'][x]['robot']['robot_hits'] += d['days'][x]['device_hits']['bots'] 
        if 'others' in d['days'][x]['device_hits']:
            d['v0001']['days'][x]['robot']['robot_hits'] += d['days'][x]['device_hits']['others'] 
            
        d['v0001']['days'][x]['quality'] = {}
        if 'quality' in d['days'][x]:
            d['v0001']['days'][x]['quality'] = d['days'][x]['quality'] 

    # write updated statistic file:
    tstat = statfile.replace('.json','v0001.json')
    
    with open(tstat, "w") as sf:
       json.dump(d,sf)
    return

        


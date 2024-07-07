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
            
        d['v0001']['days'][x]['user']['bytesSent'] = 0
        if 'bytes_sent' in d['days'][x]:
            d['v0001']['days'][x]['user']['bytesSent'] = d['days'][x]['bytes_sent']
            
        d['v0001']['days'][x]['user']['countryHits'] = d['days'][x]['countries']
        
        d['v0001']['days'][x]['user']['deviceHits'] = {}
        d['v0001']['days'][x]['user']['deviceHits']['desktop'] = d['days'][x]['device_hits']['desktop']
        d['v0001']['days'][x]['user']['deviceHits']['mobile'] = d['days'][x]['device_hits']['mobile']
        d['v0001']['days'][x]['user']['deviceHits']['tablet'] = d['days'][x]['device_hits']['tablet']
        
        d['v0001']['days'][x]['user']['externalFriendsHits'] = {}
        if 'friends' in d['days'][x]:
            d['v0001']['days'][x]['user']['externalFriendsHits'] = d['days'][x]['friends']
        d['v0001']['days'][x]['user']['topUrl'] = {}
        if 'topurl' in d['days'][x]:
            d['v0001']['days'][x]['user']['topUrl'] = d['days'][x]['topurl']
            
        d['v0001']['days'][x]['user']['serverResponseCode'] = {}
        if 'serverResponseCode' in d['days'][x]:
            d['v0001']['days'][x]['user']['serverResponseCode'] = d['days'][x]['serverResponseCode']

        d['v0001']['days'][x]['robot'] = {}
        d['v0001']['days'][x]['robot']['bytesSent'] = 0
        d['v0001']['days'][x]['robot']['robotHits'] = 0
        if 'bots' in d['days'][x]['device_hits']:
            d['v0001']['days'][x]['robot']['robotHits'] += d['days'][x]['device_hits']['bots'] 
        if 'others' in d['days'][x]['device_hits']:
            d['v0001']['days'][x]['robot']['robotHits'] += d['days'][x]['device_hits']['others'] 
            
        d['v0001']['days'][x]['quality'] = {}
        if 'quality' in d['days'][x]:
            d['v0001']['days'][x]['quality'] = d['days'][x]['quality'] 
                d['v0001']['days'][x]['user']['serverResponseCode'] = {}

    # write updated statistic file:
    tstat = statfile.replace('.json','v0001.json')
    
    with open(tstat, "w") as sf:
       json.dump(d,sf)
    return

        


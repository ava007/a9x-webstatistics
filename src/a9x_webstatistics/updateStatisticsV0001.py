from urllib.parse import urlparse
def updV0001(
    d,
    i,
    visitIP,
    domain      # own domain
    ):

    # omit css and images
    if i['request'].endswith(('.css', '.ico', '.jpg', '.jpeg', '.png','.json','.txt')):
        return d, visitIP

    owndomain = domain.replace('http://','')
    owndomain = owndomain.replace('https://','')
    owndomain = owndomain.replace('www.','')
        
    dt = i['ymd']

    # init a new day with minimal attributes:
    if 'v0001' not in d:
        d['v0001'] = {}
    if 'days' not in d['v0001']:
        d['v0001']['days'] = {}
    if dt not in d['v0001']['days']:
        d['v0001']['days'][dt] = {}
        d['v0001']['days'][dt]['user'] = {}
        d['v0001']['days'][dt]['user']['visits']  = 0
        d['v0001']['days'][dt]['user']['bytesSent'] = 0

        d['v0001']['days'][dt]['user']['deviceHits'] = {}
        d['v0001']['days'][dt]['user']['deviceHits']['mobile']  = 0 
        d['v0001']['days'][dt]['user']['deviceHits']['tablet']  = 0 
        d['v0001']['days'][dt]['user']['deviceHits']['desktop'] = 0 
        d['v0001']['days'][dt]['user']['serverResponseCode'] = {}

        d['v0001']['days'][dt]['robot'] = {}
        d['v0001']['days'][dt]['robot']['robotHits'] = 0
        d['v0001']['days'][dt]['robot']['bytesSent'] = 0
        d['v0001']['days'][dt]['robot']['serverResponseCode'] = {}
        d['v0001']['days'][dt]['quality'] = {}

    devCla = detectDeviceClass(i['user_agent']) 
    # update statistics for user:
    if devCla in ('desktop','mobile','tablet'):
        d['v0001']['days'][dt]['user']['bytesSent'] += int(i['bytes_sent'])

        if i['status'] in d['v0001']['days'][dt]['user']['serverResponseCode']:
            d['v0001']['days'][dt]['user']['serverResponseCode'][i['status']] += 1
        else:
            d['v0001']['days'][dt]['user']['serverResponseCode'][i['status']] = 1

        # process country if available:
        if 'country' in i:
            if 'countryHits' not in d['v0001']['days'][dt]['user']:
                d['v0001']['days'][dt]['user']['countryHits'] = {}
            if i['country'] not in d['v0001']['days'][dt]['user']['countryHits']:
                d['v0001']['days'][dt]['user']['countryHits'][i['country']] = 0
            d['v0001']['days'][dt]['user']['countryHits'][i['country']] += 1

        # update hits for device types:
        if devCla not in d['v0001']['days'][dt]['user']['deviceHits']:
            d['v0001']['days'][dt]['user']['deviceHits'][devCla] = 0 
        d['v0001']['days'][dt]['user']['deviceHits'][devCla] += 1 
                    
        d['timelastrec'] = i['timestamp']

        # update visits
        if i['ip'] not in visitIP :
            d['v0001']['days'][dt]['user']['visits'] = d['v0001']['days'][dt]['user']['visits'] + 1;
            visitIP[i['ip']] = 1

        # top urls: accumulate top urls
        # todo: omit query string
        if i['status'] == '200':
            if 'topUrl' not in d['v0001']['days'][dt]['user']:
                d['v0001']['days'][dt]['user']['topUrl'] = {}
            if i['request'] not in d['v0001']['days'][dt]['user']['topUrl']:
                d['v0001']['days'][dt]['user']['topUrl'][i['request']] = 0
            d['v0001']['days'][dt]['user']['topUrl'][i['request']] += 1

        # update friends on the first day of the month:
        if i['status'] == '200' and len(i['referer']) > 1 and i['referer'][0:4] == 'http' and owndomain not in i['referer']:
            refurl = urlparse(i['referer']).netloc
            rdomain = refurl.removeprefix('www.')
            rdomain = rdomain.removesuffix(':80')    # to avoid duplicates: with or without ports
            if 'externalFriendsHits' not in d['v0001']['days'][dt]['user']:
                d['v0001']['days'][dt]['user']['externalFriendsHits'] = {}
            if rdomain not in d['v0001']['days'][dt]['user']['externalFriendsHits']:
                d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain] = {'cnt': 0, 'target': {} }
            if i['request'] not in d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain]['target']:
                d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain]['target'][i['request']] = 0
            d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain]['target'][i['request']] += 1
            d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain]['cnt'] += 1
         
    # update statistics for ROBOTS:
    if devCla not in ('desktop','mobile','tablet'):
        d['v0001']['days'][dt]['robot']['bytesSent'] += int(i['bytes_sent'])
        d['v0001']['days'][dt]['robot']['robotHits'] += 1
        
        if i['status'] in d['v0001']['days'][dt]['robot']['serverResponseCode']:
            d['v0001']['days'][dt]['robot']['serverResponseCode'][i['status']] += 1
        else:
            d['v0001']['days'][dt]['robot']['serverResponseCode'][i['status']] = 1
        
    # update quality: internal server error
    if i['status'] == '500':
        if 'quality' not in d['v0001']['days'][dt]:
            d['v0001']['days'][dt]['quality'] = {}
        if i['request'] not in d['v0001']['days'][dt]['quality']:
            d['v0001']['days'][dt]['quality'][i['request']] = {}
            d['v0001']['days'][dt]['quality'][i['request']]['from'] = i['referer']
            d['v0001']['days'][dt]['quality'][i['request']]['status'] = i['status']
            d['v0001']['days'][dt]['quality'][i['request']]['count'] = 1
            d['v0001']['days'][dt]['quality'][i['request']]['comment'] = 'internal server error'
        else:
            d['v0001']['days'][dt]['quality'][i['request']]['count'] += 1

    # update quality: internal permanently redirects: 301
    if len(i['referer']) > 1 and (i['status'] == '301'):
        if 'quality' not in d['v0001']['days'][dt]:
            d['v0001']['days'][dt]['quality'] = {}
        if i['request'] not in d['v0001']['days'][dt]['quality']:
            d['v0001']['days'][dt]['quality'][i['request']] = {}
            d['v0001']['days'][dt]['quality'][i['request']]['from'] = i['referer']
            d['v0001']['days'][dt]['quality'][i['request']]['status'] = i['status']
            d['v0001']['days'][dt]['quality'][i['request']]['count'] = 1
            d['v0001']['days'][dt]['quality'][i['request']]['comment'] = 'internal permanent redirect'
        else:
            d['v0001']['days'][dt]['quality'][i['request']]['count'] += 1

    # update quality: internal not found    
    if len(i['referer']) > 1 and (i['status'] == '404'):
        if 'quality' not in d['v0001']['days'][dt]:
            d['v0001']['days'][dt]['quality'] = {}
        if i['request'] not in d['v0001']['days'][dt]['quality']:
            d['v0001']['days'][dt]['quality'][i['request']] = {}
            d['v0001']['days'][dt]['quality'][i['request']]['from'] = i['referer']
            d['v0001']['days'][dt]['quality'][i['request']]['status'] = i['status']
            d['v0001']['days'][dt]['quality'][i['request']]['count'] = 1
            d['v0001']['days'][dt]['quality'][i['request']]['comment'] = 'internal not found'
        else:
            d['v0001']['days'][dt]['quality'][i['request']]['count'] += 1

    # accumulate user navigation on first day of the month
    if len(i['referer']) > 1 and (i['status'] == '200') and devCla in ('desktop','mobile','tablet'):
        oref = urlparse(i['referer'])   # remove query string...
        oreq = urlparse(i['request'])   # remove query string...
        dt01 = i['ymd'][0:6] + '01'

        # on the very first run during the month, make sure that the structure exists:
        if dt01 not in d['v0001']['days']:
            d['v0001']['days'][dt01] = {}
            d['v0001']['days'][dt01]['user'] = {}
            
        if 'navigation' not in d['v0001']['days'][dt01]['user']:
           d['v0001']['days'][dt01]['user']['navigation'] = {}
        nkey = oref.path + '(())' + oreq.path
        if nkey not in d['v0001']['days'][dt01]['user']['navigation']:
           d['v0001']['days'][dt01]['user']['navigation'][nkey] = 0
        d['v0001']['days'][dt01]['user']['navigation'][nkey] += 1

        # cleanup
        for ck,cv in d['v0001']['days'][dt01]['user']['navigation'].items():
           print("nav: " + str(ck) + " " + str(cv) )

    return d, visitIP

def detectDeviceClass(ua):
  if ua is None:
     return 'others'
  if (ua.lower().find('bot') > 0):
     return 'bots'
  if (ua.lower().find('externalhit') > 0):  # facebook
     return 'bots'
  if (ua.lower().find('spider') > 0):  # bytedance
     return 'bots'
  if (ua.lower().find('crawler') > 0):
     return 'others'
  if (ua.lower().find('python') > 0):
     return 'bots'
  if (ua.lower().find('mediapartner') > 0):
     return 'others'
  if (ua.lower().find('curl') > 0):
     return 'others'
  if (ua.lower().find('ipad') > 0):
     return 'tablet'
  if (ua.lower().find('mobile') > 0):
     return 'mobile'
  if (ua.lower().find('android') > 0):
     return 'tablet'
  return 'desktop'

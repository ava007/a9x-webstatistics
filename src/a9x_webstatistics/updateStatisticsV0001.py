from urllib.parse import urlparse
def updV0001(
    d,
    i,
    visitIP,
    domain      # own domain
    ):

    # omit css, ico etc
    if i['request'].endswith(('.css', '.ico', '.jpg')):
        return d, visitIP
        
    dt = i['ymd']

    # init a new day with minimal attributes:
    if 'v0001' not in d:
        d['v0001'] = {}
    if 'days' not in d['v0001']:
        d['v0001']['days'] = {}
    if dt not in d['v0001']['days']:
        d['v0001']['days'][dt] = {}
        d['v0001']['days'][dt]['user']    = {};
        d['v0001']['days'][dt]['user']['visits']  = 0;
        d['v0001']['days'][dt]['user']['bytesSent'] = 0;

        d['v0001']['days'][dt]['user']['deviceHits'] = {}
        d['v0001']['days'][dt]['user']['deviceHits']['mobile']  = 0 
        d['v0001']['days'][dt]['user']['deviceHits']['tablet']  = 0 
        d['v0001']['days'][dt]['user']['deviceHits']['desktop'] = 0 
        d['v0001']['days'][dt]['user']['serverResponseCode'] = {}

        d['v0001']['days'][dt]['robot']    = {};
        d['v0001']['days'][dt]['robot']['robotHits']  = 0;
        d['v0001']['days'][dt]['robot']['bytesSent'] = 0;
        d['v0001']['days'][dt]['robot']['serverResponseCode'] = {}
        d['v0001']['days'][dt]['quality']    = {};

    devCla = detectDeviceClass(i['user_agent']) 
    # update statistics for user:
    if devCla in ('desktop','mobile','tablet'):
        #d['v0001']['days'][dt]['hits'] = d['days'][dt]['hits'] + 1
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
                d['v0001']['days'][dt]['user']['countryHits'][i['country']] = 0;
            d['v0001']['days'][dt]['user']['countryHits'][i['country']] += 1;

        # update hits for device types:
        if devCla not in d['v0001']['days'][dt]['user']['deviceHits']:
            d['v0001']['days'][dt]['user']['deviceHits'][devCla] = 0 
        d['v0001']['days'][dt]['user']['deviceHits'][devCla] += 1 

        # update external source:
        #if 'referer' in i and i['referer'] != "-":
        #    if 'externalFriendsHits' not in d['v0001']['days'][dt]['user']:
        #        d['v0001']['days'][dt]['user']['externalFriendsHits'] = {}
        #    refurl = urlparse(i['referer']).netloc
        #    rdomain = refurl.removeprefix('www.')
        #    if rdomain not in d['days'][dt]['user']['externalFriendsHits']:
        #        d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain] = 0;
        #    d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain] += 1;
                    
        d['timelastrec'] = i['timestamp']

        # update visits
        if i['ip'] not in visitIP :
            d['v0001']['days'][dt]['user']['visits'] = d['v0001']['days'][dt]['user']['visits'] + 1;
            visitIP[i['ip']] = 1

        # top urls: accumulate top urls on the first day of the month
        dtTopUrl = dt[0:6] + '01'
        if i['status'] == '200':
            if 'topUrl' not in d['v0001']['days'][dtTopUrl]['user']:
                d['v0001']['days'][dtTopUrl]['user']['topUrl'] = {}
            if i['request'] not in d['v0001']['days'][dtTopUrl]['user']['topUrl']:
                d['v0001']['days'][dtTopUrl]['user']['topUrl'][i['request']] = 0;
            d['v0001']['days'][dtTopUrl]['user']['topUrl'][i['request']] += 1;

        # update friends on the first day of the month:
        dtFriends = dt[0:6] + '01'
        if i['status'] == '200' and len(i['referer']) > 1 and i['referer'][0:4] == 'http' and domain not in i['referer']:
            refurl = urlparse(i['referer']).netloc
            rdomain = refurl.removeprefix('www.')
            if 'externalFriendsHits' not in d['v0001']['days'][dtFriends]['user']:
                d['v0001']['days'][dtFriends]['user']['externalFriendsHits'] = {}
            if rdomain not in d['v0001']['days'][dtFriends]['user']['externalFriendsHits']:
                d['v0001']['days'][dtFriends]['user']['externalFriendsHits'][rdomain] = {'cnt': 0, 'target': {} };
            if i['request'] not in d['v0001']['days'][dtFriends]['user']['externalFriendsHits'][rdomain]['target']:
                d['v0001']['days'][dtFriends]['user']['externalFriendsHits'][rdomain]['target'][i['request']] = 0
            d['v0001']['days'][dtFriends]['user']['externalFriendsHits'][rdomain]['target'][i['request']] += 1
            d['v0001']['days'][dtFriends]['user']['externalFriendsHits'][rdomain]['cnt'] += 1
         
    # update statistics for ROBOTS:
    if devCla not in ('desktop','mobile','tablet'):
        d['v0001']['days'][dt]['robot']['bytesSent'] += int(i['bytes_sent'])
        d['v0001']['days'][dt]['robot']['robotHits'] += 1
        
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
        if 'quality' not in d['days'][dt]:
            d['v0001']['days'][dt]['quality'] = {}
        if i['request'] not in d['days'][dt]['quality']:
            d['v0001']['days'][dt]['quality'][i['request']] = {}
            d['v0001']['days'][dt]['quality'][i['request']]['from'] = i['referer']
            d['v0001']['days'][dt]['quality'][i['request']]['status'] = i['status']
            d['v0001']['days'][dt]['quality'][i['request']]['count'] = 1
            d['v0001']['days'][dt]['quality'][i['request']]['comment'] = 'internal permanent redirect'
        else:
            d['v0001']['days'][dt]['quality'][i['request']]['count'] += 1

    # update quality: internal not found    
    if len(i['referer']) > 1 and (i['status'] == '404'):
        if 'quality' not in d['days'][dt]:
            d['v0001']['days'][dt]['quality'] = {}
        if i['request'] not in d['v0001']['days'][dt]['quality']:
            d['v0001']['days'][dt]['quality'][i['request']] = {}
            d['v0001']['days'][dt]['quality'][i['request']]['from'] = i['referer']
            d['v0001']['days'][dt]['quality'][i['request']]['status'] = i['status']
            d['v0001']['days'][dt]['quality'][i['request']]['count'] = 1
            d['v0001']['days'][dt]['quality'][i['request']]['comment'] = 'internal not found'
        else:
            d['v0001']['days'][dt]['quality'][i['request']]['count'] += 1

    return d, visitIP

def detectDeviceClass(ua):
  if ua is None:
     return 'others'
  if (ua.lower().find('bot') > 0):
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

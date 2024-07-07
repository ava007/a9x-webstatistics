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
    if dt not in d['days']:
        d['v0001']['days'][dt] = {}
        d['v0001']['days'][dt]['hits']    = 0;
        d['v0001']['days'][dt]['visits']  = 0;
        d['v0001']['days'][dt]['bytes_sent'] = 0;
        d['v0001']['days'][dt]['serverResponseCode'] = {}
        d['v0001']['days'][dt]['device_hits'] = {} 
        d['v0001']['days'][dt]['device_hits']['mobile']  = 0 
        d['v0001']['days'][dt]['device_hits']['tablet']  = 0 
        d['v0001']['days'][dt]['device_hits']['desktop'] = 0 
        d['v0001']['days'][dt]['device_hits']['bots']    = 0 
        d['v0001']['days'][dt]['device_hits']['others']  = 0 

    # update statistics
    d['v0001']['days'][dt]['hits'] = d['days'][dt]['hits'] + 1
    d['v0001']['days'][dt]['bytes_sent'] = str(int(d['days'][dt]['bytes_sent']) + int(i['bytes_sent']))

    if i['status'] in d['v0001']['days'][dt]['serverResponseCode']:
        d['v0001']['days'][dt]['serverResponseCode'][i['status']] += 1
    else:
        d['v0001']['days'][dt]['serverResponseCode'][i['status']] = 1

    # process country if available:
    if 'country' in i:
        if 'countries' not in d['days'][dt]:
            d['v0001']['days'][dt]['countries'] = {}
        if i['country'] not in d['v0001']['days'][dt]['countries']:
            d['v0001']['days'][dt]['countries'][i['country']] = 0;
        d['v0001']['days'][dt]['countries'][i['country']] = d['v0001']['days'][dt]['countries'][i['country']] + 1;

    # update hits for device types:
    devCla = detectDeviceClass(i['user_agent']) 
    if devCla not in d['v0001']['days'][dt]['device_hits']:
        d['v0001']['days'][dt]['device_hits'][devCla] = 0 
    d['v0001']['days'][dt]['device_hits'][devCla] = d['v0001']['days'][dt]['device_hits'][devCla] + 1 

    # update external source:
    if 'referer' in i and i['referer'] != "-":
        if 'source' not in d['v0001']['days'][dt]:
            d['v0001']['days'][dt]['source'] = {}
        refurl = urlparse(i['referer']).netloc
        rdomain = refurl.removeprefix('www.')
        if rdomain not in d['days'][dt]['source']:
            d['v0001']['days'][dt]['source'][rdomain] = 0;
        d['v0001']['days'][dt]['source'][rdomain] += 1;
                    
    d['timelastrec'] = i['timestamp']

    # update visits
    if i['ip'] not in visitIP and devCla in ('desktop','mobile','tablet'):
        d['v0001']['days'][dt]['visits'] = d['v0001']['days'][dt]['visits'] + 1;
        visitIP[i['ip']] = 1

    # top urls: accumulate top urls on the first day of the month
    dtTopUrl = dt[0:6] + '01'
    if i['status'] == '200' and devCla in ('desktop','mobile','tablet'):
        if 'topurl' not in d['v0001']['days'][dtTopUrl]:
            d['v0001']['days'][dtTopUrl]['topurl'] = {}
        if i['request'] not in d['v0001']['days'][dtTopUrl]['topurl']:
            d['v0001']['days'][dtTopUrl]['topurl'][i['request']] = 0;
        d['v0001']['days'][dtTopUrl]['topurl'][i['request']] += 1;

    # update friends on the first day of the month:
    dtFriends = dt[0:6] + '01'
    if i['status'] == '200' and devCla in ('desktop','mobile','tablet') and len(i['referer']) > 1 and i['referer'][0:4] == 'http' and domain not in i['referer']:
        refurl = urlparse(i['referer']).netloc
        rdomain = refurl.removeprefix('www.')
        if 'friends' not in d['v0001']['days'][dtFriends]:
            d['v0001']['days'][dtFriends]['friends'] = {}
        if rdomain not in d['v0001']['days'][dtFriends]['friends']:
            d['v0001']['days'][dtFriends]['friends'][rdomain] = {'cnt': 0, 'target': {} };
        if i['request'] not in d['v0001']['days'][dtFriends]['friends'][rdomain]['target']:
            d['v0001']['days'][dtFriends]['friends'][rdomain]['target'][i['request']] = 0
        d['v0001']['days'][dtFriends]['friends'][rdomain]['target'][i['request']] += 1
        d['v0001']['days'][dtFriends]['friends'][rdomain]['cnt'] += 1
         
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

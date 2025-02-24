from urllib.parse import urlparse
from operator import itemgetter
import ipaddress

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

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
    req = urlparse(i['request'])

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

        # top urls: accumulate top urls - omitting query strings
        if i['status'] == '200':
            if 'topUrl' not in d['v0001']['days'][dt]['user']:
                d['v0001']['days'][dt]['user']['topUrl'] = {}
            if req.path not in d['v0001']['days'][dt]['user']['topUrl']:
                d['v0001']['days'][dt]['user']['topUrl'][req.path] = 0
            d['v0001']['days'][dt]['user']['topUrl'][req.path] += 1

        # update nav:
        if (i['status'] == '200' 
            and len(i['referer']) > 1 
            and devCla in ('desktop','mobile','tablet') ):
            refurl = urlparse(i['referer']).netloc
            if 'nav' not in d['v0001']['days'][dt]['user']:
                d['v0001']['days'][dt]['user']['nav'] = []
            tmpnav = {}
            tmpnav['s'] = None       # Source
            tmpnav['t'] = req.path  # Target
            tmpnav['c'] = 1         # count
            
            # external nav
            if (i['referer'][0:4] == 'http'):
                rdomain = refurl.removeprefix('www.')
                rdomain = rdomain.removesuffix(':80')    # to avoid duplicates: with or without ports
                # omit subdomains:
                if (rdomain.count('.') > 1 
                    and is_valid_ip(rdomain) == False):
                    rdomain_ar = rdomain.split('.')
                    rdomain = rdomain_ar[-2] + '.' + rdomain_ar[-1]
                tmpnav['s'] = rdomain   # Source
                tmpnav['p'] = 'e'  # type: e=external source, i=internal source
            
            # internal nav
            else:
                #tmpnav['p'] = 'i'  # type: e=external source, i=internal source
                tmpnav['s'] = req.path   # Source

            if (tmpnav['s'] is not None 
                and tmpnav['t'] is not None):
                found = False        
                for e in d['v0001']['days'][dt]['user']['nav']:
                    if (e['s'] == tmpnav['s']
                        and e['t'] == tmpnav['t']):
                        e['c'] += tmpnav['c']
                        found = True
                        break
                if found == False:
                    d['v0001']['days'][dt]['user']['nav'].append(tmpnav)

            
        # update friends:
        #if i['status'] == '200' and len(i['referer']) > 1 and i['referer'][0:4] == 'http' and owndomain not in i['referer']:
        #    refurl = urlparse(i['referer']).netloc
        #    rdomain = refurl.removeprefix('www.')
        #    rdomain = rdomain.removesuffix(':80')    # to avoid duplicates: with or without ports
            # omit subdomains:
        #    if (rdomain.count('.') > 1 
        #            and is_valid_ip(rdomain) == False):
        #        rdomain_ar = rdomain.split('.')
        #        rdomain = rdomain_ar[-2] + '.' + rdomain_ar[-1]
                
        #    if (is_valid_ip(rdomain) == False 
        #            and '[' not in rdomain):  # to suppress ip; ip is not a domain anyway
        #        if 'externalFriendsHits' not in d['v0001']['days'][dt]['user']:
        #            d['v0001']['days'][dt]['user']['externalFriendsHits'] = {}
        #        if rdomain not in d['v0001']['days'][dt]['user']['externalFriendsHits']:
        #            d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain] = {'cnt': 0, 'target': {} }
        #        if i['request'] not in d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain]['target']:
        #            d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain]['target'][req.path] = 0
        #        d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain]['target'][req.path] += 1
        #        d['v0001']['days'][dt]['user']['externalFriendsHits'][rdomain]['cnt'] += 1
         
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
    if (len(i['referer']) > 1
            and i['status'] == '301'
            and devCla in ('desktop','mobile','tablet')):
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
    if (len(i['referer']) > 1 
            and i['status'] == '404'
            and devCla in ('desktop','mobile','tablet')):
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

    # accumulate user navigation 
    #if (len(i['referer']) > 1 
    #        and i['status'] == '200'
    #        and devCla in ('desktop','mobile','tablet')):
    #    oref = urlparse(i['referer'])   # remove query string...
    #    oreq = urlparse(i['request'])   # remove query string...
            
    #    if 'navigation' not in d['v0001']['days'][dt]['user']:
    #       d['v0001']['days'][dt]['user']['navigation'] = {}
    #    nkey = oref.path + '(())' + oreq.path
    #    if nkey not in d['v0001']['days'][dt]['user']['navigation']:
    #       d['v0001']['days'][dt]['user']['navigation'][nkey] = 0
    #    d['v0001']['days'][dt]['user']['navigation'][nkey] += 1

        # cleanup: delete entry from long tail...
        #z = 1
        #for ck,cv in sorted(d['v0001']['days'][dt01]['user']['navigation'].items(), key=itemgetter(1), reverse=True):
        #   z += 1
        #   if z > 100 and cv == 1:
        #      #print("nav: " + str(ck) + " " + str(cv) +  " --> deleted")
        #      del d['v0001']['days'][dt01]['user']['navigation'][ck]

    # cache status for all successful requests:
    if ('cache_status' in i 
            and i['status'] == '200'):
        if len(i['cache_status']) == 0:  # avoid empty values
            i['cache_status'] = 'unknown'
        if 'performance' not in d['v0001']['days'][dt]:
           d['v0001']['days'][dt]['performance'] = {} 
        if 'cache' not in d['v0001']['days'][dt]['performance']:
           d['v0001']['days'][dt]['performance']['cache'] = {} 
        if i['cache_status'] not in d['v0001']['days'][dt]['performance']['cache']:
            d['v0001']['days'][dt]['performance']['cache'][i['cache_status']] = 1
        else:
            d['v0001']['days'][dt]['performance']['cache'][i['cache_status']] += 1

    # response time:
    if ('response_time' in i 
            and len(i['response_time']) > 0):
        tmp_rtime = float(i['response_time'])
        if tmp_rtime > 0:
            if 'performance' not in d['v0001']['days'][dt]:
               d['v0001']['days'][dt]['performance'] = {} 
            if 'response_time' not in d['v0001']['days'][dt]['performance']:
               d['v0001']['days'][dt]['performance']['response_time'] = {'time_count': 0, 'time_sum': 0} 
            d['v0001']['days'][dt]['performance']['response_time']['time_sum'] += tmp_rtime
            d['v0001']['days'][dt]['performance']['response_time']['time_count'] += 1

            # top x fastest:
            if 'topFast' not in d['v0001']['days'][dt]['performance']:
                d['v0001']['days'][dt]['performance']['topFast'] = {} 
                d['v0001']['days'][dt]['performance']['topFast'][i['request']] = tmp_rtime
            else:
                max_value = float(max(d['v0001']['days'][dt]['performance']['topFast'].values()))  # maximum value
                if tmp_rtime  < max_value:
                    d['v0001']['days'][dt]['performance']['topFast'][i['request']] = tmp_rtime

                if len(d['v0001']['days'][dt]['performance']['topFast']) > 5:
                    tmpFast = dict(sorted(d['v0001']['days'][dt]['performance']['topFast'].items(), key=lambda item: item[1], reverse=False))
                    z = 0
                    d['v0001']['days'][dt]['performance']['topFast'] = {}
                    for k,v in tmpFast.items():
                        z += 1
                        if z >= 5:
                            break
                        d['v0001']['days'][dt]['performance']['topFast'][k] = v
                    del tmpFast

            # top Slowest:
            if 'topSlow' not in d['v0001']['days'][dt]['performance']:
                d['v0001']['days'][dt]['performance']['topSlow'] = {} 
                d['v0001']['days'][dt]['performance']['topSlow'][i['request']] = tmp_rtime
            else:
                min_value = float(min(d['v0001']['days'][dt]['performance']['topSlow'].values()))  # minimum value
                if tmp_rtime > min_value:
                    d['v0001']['days'][dt]['performance']['topSlow'][i['request']] = tmp_rtime

            if len(d['v0001']['days'][dt]['performance']['topSlow']) > 5:
                tmpSlow = dict(sorted(d['v0001']['days'][dt]['performance']['topSlow'].items(), key=lambda item: item[1], reverse=True))
                z = 0
                d['v0001']['days'][dt]['performance']['topSlow'] = {}
                for k,v in tmpSlow.items():
                    z += 1
                    if z >= 5:
                        break
                    d['v0001']['days'][dt]['performance']['topSlow'][k] = v
                del tmpSlow
    
    # accept language for user hits only:
    # ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
    # en
    # en-US,en;q=0.5
    # de,en-US;q=0.7,en;q=0.3
    # zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
    tmp_lang = []
    if i['status'] == '200' and 'accept_language' in i and len(i['accept_language']) > 0 and devCla in ('desktop','mobile','tablet'):
        if 'language' not in d['v0001']['days'][dt]['user']:
            d['v0001']['days'][dt]['user']['language'] = {}
        for k,v in i['accept_language'].items():
            lng = k[0:2]  # take language only, ignore country
            # count each language only once per hit:
            if lng not in tmp_lang:
                tmp_lang.append(lng)
                if lng not in d['v0001']['days'][dt]['user']['language']:
                    d['v0001']['days'][dt]['user']['language'][lng] = 0
                d['v0001']['days'][dt]['user']['language'][lng] += 1
    #print("\nd: " + str(dt) + " "  + str(d['v0001']['days'][dt]) ) 
                
    return d, visitIP

def detectDeviceClass(ua):
  if ua is None:
     return 'others'
  if (ua.lower().find('bot') > 0):
     return 'bots'
  if (ua.lower().find('externalhit') > 0):    # facebook
     return 'bots'
  if (ua.lower().find('spider') > 0):        # bytedance
     return 'bots'
  if (ua.lower().find('crawler') > 0):
     return 'others'
  if (ua.lower().find('python') > 0):        # python-requests
     return 'bots'
  if (ua.lower().find('mediapartner') > 0):
     return 'others'
  if (ua.lower().find('feedly') > 0):        # Feedly
     return 'bots'
  if (ua.lower().find('validator') > 0):     # validator
     return 'bots'
  if (ua.lower().find('curl') > 0):
     return 'others'
  if (ua.lower().find('ipad') > 0):
     return 'tablet'
  if (ua.lower().find('mobile') > 0):
     return 'mobile'
  if (ua.lower().find('android') > 0):
     return 'tablet'
  return 'desktop'

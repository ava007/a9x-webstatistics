import ast
from datetime import datetime

def parseRecJsonV0001(rec):
    r = ast.literal_eval(rec)    # parse rec to dict

    # local time:
    if 'time_local' in r:
        dto = datetime.strptime(r['time_local'], "%d/%b/%Y:%H:%M:%S %z")   # 07/Jan/2024:14:06:24 +0000
    elif 'tl' in r:
        dto = datetime.strptime(r['tl'], "%d/%b/%Y:%H:%M:%S %z")   # 07/Jan/2024:14:06:24 +0000
    else:
        raise Exception("no remote addr found in input file")

    ret = {
        'ymd': dto.strftime("%Y%m%d"),
        'timestamp': dto.strftime("%Y%m%d%H%M%S"),
        'referer': ''
    }

    # remote address IPv4 or IPv6:
    if 'ra' in r:
        ret['ip'] = r['ra']
    elif 'ip' in r:
        ret['ip'] = r['ip']
    elif 'remote_addr' in r:
        ret['ip'] = r['remote_addr']
    else:
        raise Exception("no remote addr found in input file")

    # request:
    if 'rq' in r:
        ret['request'] = r['rq']
    elif 'request' in r:
        ret['request'] = r['request']
    else:
        raise Exception("no request found in input file")
    
    if 'status' in r:
       ret['status'] = r['status']
    if 'st' in r:
       ret['status'] = r['st']

    if 'bytes_sent' in r:
        ret['bytes_sent'] = r['bytes_sent']
    if 'bs' in r:
        ret['bytes_sent'] = r['bytes_sent']
        
    if 'rf' in r:
         ret['referer'] =  r['referer']
    
    if 'http_user_agent' in r: 
        ret['user_agent'] = r['http_user_agent']
    if 'ua' in r: 
        ret['user_agent'] = r['ua']
   
    # collect the optional attributes:
    if 'rt' in r:
        ret['request_time'] = r['rt']
    if 'request_time' in r:
        ret['request_time'] = r['request_time']

    if 'upstream_respone_time' in r:
        ret['response_time'] = r['upstream_respone_time']
    if 'rt' in r:
        ret['response_time'] = r['rt']
    
    if 'upstream_cache_status' in r:
        ret['cache_status'] = r['upstream_cache_status']
    if 'cs' in r:
        ret['cache_status'] = r['cs']
    
    if 'http_accept_language' in r:
        ret['accept_language'] = r['http_accept_language']
    if 'al' in r:
        ret['accept_language'] = r['al']
   

    return ret

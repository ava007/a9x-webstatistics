import ast
from datetime import datetime

def parseRecJsonV0001(rec):
    r = ast.literal_eval(rec)    # parse rec to dict
    dto = datetime.strptime(r['time_local'], "%d/%b/%Y:%H:%M:%S %z")   # 07/Jan/2024:14:06:24 +0000

    # skip already processed data:
    #if dto  <=  lasttimerecobj:
    #    return
        
    ret = {
            'ip': r['remote_addr'],
            'ymd': dto.strftime("%Y%m%d"),
            'timestamp': dto.strftime("%Y%m%d%H%M%S") ,
            'request': r['request'],
            'status': r['status'],
            'bytes_sent': r['bytes_sent'],
            'referer': r['referer'],
            'user_agent': r['http_user_agent']
        }
    if r['upstream_respone_time'] is not None:
        ret['response_time'] = r['upstream_respone_time']
    if r['upstream_cache_status'] is not None:
        ret['cache_status'] = r['upstream_cache_status']
    if r['http_accept_language'] is not None:
        ret['accept_language'] = r['http_accept_language']

    return ret

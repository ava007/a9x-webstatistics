import ast
#import io, sys, argparse, json, ast

def(rec, lasttimerecobj, georeader):
    r = ast.literal_eval(rec)    # parse rec to dict
    dto = datetime.strptime(r['time_local'], "%d/%b/%Y:%H:%M:%S %z")   # 07/Jan/2024:14:06:24 +0000

    # skip already processed data:
    if dto  <=  lasttimerecobj:
        continue

    if georeader:
        try:
            grrsp = georeader.country(r['remote_addr'])
            country = grrsp.country.name
        except geoip2.errors.AddressNotFoundError:
            country = None
    else:
        country = None
        
    ret = {
            'ip': r['remote_addr'],
            'ymd': dto.strftime("%Y%m%d"),
            'timestamp': dto.strftime("%Y%m%d%H%M%S") ,
            'request': r['request'],
            'status': r['status'],
            'bytes_sent': r['bytes_sent'],
            'referer': r['referer'],
            'user_agent': r['user_agent']
        }
    if country:
        r['country'] = country

    return ret

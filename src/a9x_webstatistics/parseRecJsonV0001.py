import ast
import geoip2.database
from datetime import datetime

def parseRecJsonV0001(rec, georeader):
    r = ast.literal_eval(rec)    # parse rec to dict

    # local time:
    if 'time_local' in r:
        dto = datetime.strptime(r['time_local'], "%d/%b/%Y:%H:%M:%S %z")   # 07/Jan/2024:14:06:24 +0000
    elif 'tl' in r:
        dto = datetime.strptime(r['tl'], "%d/%b/%Y:%H:%M:%S %z")   # 07/Jan/2024:14:06:24 +0000
    else:
        raise Exception("no time found in input file. Details of input record: " + str(r) )

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
        raise Exception("no remote addr found in input file.   Details of input record: " + str(r))

    # request:
    if 'rq' in r:
        ret['request'] = r['rq']
    elif 'request' in r:
        ret['request'] = r['request']
    elif 'u' in r:
        ret['request'] = r['u']
    elif 'ur' in r:
        ret['request'] = r['ur']
    else:
        raise Exception("no request found in input file.   for details check input record: " + str(r))
    
    if 'status' in r:
       ret['status'] = r['status']
    if 'st' in r:
       ret['status'] = r['st']

    if 'bytes_sent' in r:
        ret['bytes_sent'] = r['bytes_sent']
    if 'bs' in r:
        ret['bytes_sent'] = r['bs']
        
    if 'rf' in r:
         ret['referer'] =  r['rf']
    if 'http_referer' in r:
         ret['referer'] =  r['http_referer']
    
    if 'http_user_agent' in r: 
        ret['user_agent'] = r['http_user_agent']
    if 'ua' in r: 
        ret['user_agent'] = r['ua']
   
    # collect the optional attributes:
    if 'rt' in r and len(r['rt']) > 0:
        ret['request_time'] = r['rt']
    if 'request_time' in r and len(r['request_time']) > 0:
        ret['request_time'] = r['request_time']

    if 'upstream_respone_time' in r and len(r['upstream_response_time']) > 0:
        ret['response_time'] = r['upstream_respone_time']
    if 'rt' in r and len(r['rt']) > 0:
        ret['response_time'] = r['rt']
    
    if 'upstream_cache_status' in r:
        ret['cache_status'] = r['upstream_cache_status']
    if 'cs' in r:
        ret['cache_status'] = r['cs']
    
    if 'http_accept_language' in r:
        ret['accept_language'] = parse_accept_language(r['http_accept_language'])
    if 'al' in r:
        ret['accept_language'] = parse_accept_language(r['al'])
   
    if georeader:
        try:
            grrsp = georeader.country(ret['ip'])
            ret['country'] = grrsp.country.name
        except geoip2.errors.AddressNotFoundError:
            pass     # ie. do nothing
   
    return ret

# 'da, en-gb;q=0.8, en;q=0.7'  meaning: "I prefer Danish, but will accept British English and other types of English"
# 'fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5'
# https://www.rfc-editor.org/rfc/rfc9110.html#name-accept-language
# https://www.rfc-editor.org/rfc/rfc4647.html
# https://www.rfc-editor.org/rfc/rfc5646.html
# Country code according to ISO3166-1 (capitalized letters)
# Language codes according to ISO639-1 (lowercase letters)

def parse_accept_language(accept_language_input):
    if not accept_language_input:
        return []

    if len(accept_language_input) > 8192:
        raise ValueError('Accept-Language exceeds maximum length of 8192 characters.')
        
    # Split the string by commas to get each language tag
    language_tags = accept_language_input.split(',')

    locales = {}
    #print("Input: " + accept_language_input)

    for tag in language_tags:
        # split locale and quality
        localeregion, _, qstr = tag.partition(';q=')
        if len(qstr) == 0:
            qstr = 1
            
        try:
            q = float(qstr or 1.0)
        except ValueError:
            continue  # ignore malformed entry

        # split locale into locale and region
        locale, _, region = localeregion.partition('-')
        
        #print("locale: " + str(locale) + " " + str(q) + " " + str(region) )
        if locale not in locales:
            locales[locale] = q
        
    #print("AL-Results: "  + str(locales))
    return locales

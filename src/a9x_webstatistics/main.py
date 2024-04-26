import argparse
import io
import json
import re
import sys
from datetime import datetime
from .updatestatistics import upd

def parseRec(rec, log_pattern):
    print(str(rec))

    r = {}
    # skip comments recs
    if rec[0:1] == '#':
        return r

    match = log_pattern.match(rec)
    if match:
        ip_address = match.group(1)
        timestamp = match.group(2)
        request = match.group(3)
        status = match.group(4)
        bytes_sent = match.group(5)
        referer = match.group(6)
        user_agent = match.group(7)

        dto = datetime.strptime(timestamp,'%d/%b/%Y:%H:%M:%S %z')  # 07/Jan/2024:14:06:24 +0000
                
        r = {
            'ip': ip_address,
            'ymd': dto.strftime("%Y%m%d"),
            'timestamp': dto.strftime("%Y%m%d%H%M%S") ,
            'request': request,
            'status': status,
            'bytes_sent': bytes_sent,
            'referer': referer,
            'user_agent': user_agent
        }
                
        return r
    

    # get date and time:  19/Apr/2024:14:49:22 +0000
    dtcomp = re.compile('\d{2}[/][A-Za-z]{3}[/]\d{4}[:]\d{2}[:]\d{2}[:]\d{2}')
    dt = dtcomp.search(rec)  # scan for first match in rec
    r['timestamp'] = datetime.strptime(dt[0],'%d/%b/%Y:%H:%M:%S')

    # get ip address:
    ip6 =   '''(?:(?x)(?:(?:[0-9a-f]{1,4}:){1,1}(?::[0-9a-f]{1,4}){1,6})|
    (?:(?:[0-9a-f]{1,4}:){1,2}(?::[0-9a-f]{1,4}){1,5})|
    (?:(?:[0-9a-f]{1,4}:){1,3}(?::[0-9a-f]{1,4}){1,4})|
    (?:(?:[0-9a-f]{1,4}:){1,4}(?::[0-9a-f]{1,4}){1,3})|
    (?:(?:[0-9a-f]{1,4}:){1,5}(?::[0-9a-f]{1,4}){1,2})|
    (?:(?:[0-9a-f]{1,4}:){1,6}(?::[0-9a-f]{1,4}){1,1})|
    (?:(?:(?:[0-9a-f]{1,4}:){1,7}|:):)|
    (?::(?::[0-9a-f]{1,4}){1,7})|
    (?:(?:(?:(?:[0-9a-f]{1,4}:){6})(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}))|
    (?:(?:(?:[0-9a-f]{1,4}:){5}[0-9a-f]{1,4}:(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}))|
    (?:(?:[0-9a-f]{1,4}:){5}:[0-9a-f]{1,4}:(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})|
    (?:(?:[0-9a-f]{1,4}:){1,1}(?::[0-9a-f]{1,4}){1,4}:(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})|
    (?:(?:[0-9a-f]{1,4}:){1,2}(?::[0-9a-f]{1,4}){1,3}:(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})|
    (?:(?:[0-9a-f]{1,4}:){1,3}(?::[0-9a-f]{1,4}){1,2}:(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})|
    (?:(?:[0-9a-f]{1,4}:){1,4}(?::[0-9a-f]{1,4}){1,1}:(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})|
    (?:(?:(?:[0-9a-f]{1,4}:){1,5}|:):(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})|
    (?::(?::[0-9a-f]{1,4}){1,5}:(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}))
    '''
    #ip4 =   '(?:[12]?\\d?\\d\\.){3}[12]?\\d?\\d'
    ip4 = '^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$'
     
    ip = re.findall(ip4 + '|' + ip6, rec)
    if not ip:
        r['ip'] = ''
        print("IP not detected in: " + rec)
    else:
        r['ip'] = ip[0]
    return r


def detectDeviceClass(ua):
  if ua is None:
     return 'desktop'
  if (ua.lower().find('bot') > 0):
     return 'bots'
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

def runws():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-s", "--statfile", help="json file that contains calculated statistics", default="webstat.json")
    parser.add_argument("-i", "--infile", help="filename including path to web server access log that contains input data", default="nginx_access.log")
    args, unknown = parser.parse_known_args()

    # init statistic file if it does not exist:
    d = {}
    d['timelastrec'] = '19991231235959'
    d['days'] = {}

    lasttimerecobj = datetime.strptime(d['timelastrec'],"%Y%m%d%H%M%S")
    print("lasttimerecobj: " + str(lasttimerecobj))

    # init job results
    j = {
        'records_read_total': 0,
        'records_skipped_comment': 0,
        'records_already_processed': 0,
        'records_processed_for_statistic': 0,
    }
    
    # load statistic file if it exists
    try:
        f = open(args.statfile) 
        d = json.load(f) 
    except FileNotFoundError:   # first call: file does not exists
        print("-s statistic file not found, it will be automatically created")
    except json.JSONDecodeError:
        print("-s json file is not valid")

    visitIP = {}

    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[0-9a-fA-F:]+'
    log_pattern = re.compile(r'({}) - - \[([^\]]+)\] "([^"]+)" (\d+) (\d+) "([^"]+)" "([^"]+)"'.format(ip_pattern))
    
    # process infile:
    with open(args.infile,'r') as infile:
        for rec in infile:
            recparsed = parseRec(rec, log_pattern)
            # skip unrecognized records:
            if not recparsed or recparsed['timestamp'] is None or recparsed['ip'] is None:
                continue
            # skip already processed data:
            if recparsed['timestamp']  <=  d['timelastrec']:
                continue
            d = upd(d, recparsed, visitIP)
            
    # write updated statistic file:
    with open(args.statfile, "w") as sf:
       json.dump(d,sf)  
    return 0

if __name__ == "__main__":
    runws()

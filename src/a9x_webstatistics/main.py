import io, sys, argparse, json
import re

def parseRec(rec):
    print(str(rec))

    r = {}
    # find ipv4 address:
    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', s )
    # find ipv6 address:
    if ip is None:
      ip = re.findall(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))
    print(str(ip))
    r['ip'] = ip[0]


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

    # init statistic file if it does not exists:
    d = {}
    d['timelastrec'] = '19991231235959'
    d['days'] = {}

    # load statistic file if it exists
    try:
        f = open(args.statfile) 
        d = json.load(f) 
    except FileNotFoundError:   # first call: file does not exists
        print("-s statistic file not found, it will be automatically created")
    except json.JSONDecodeError:
        print("-s json file is not valid")

    # process infile:
    with open(args.infile,'r') as infile:
        for rec in infile:
            parseRec(rec)

    # write updated statistic file:
    with open(args.statfile, "w") as sf:
       json.dump(d,sf)  
    return 0

if __name__ == "__main__":
    runws()

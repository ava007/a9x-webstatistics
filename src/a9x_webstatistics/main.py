import io, sys, argparse, json, ast

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
    parser.add_argument("-i", "--infile", help="filename including path to web server access log that contains input data", default="/var/log/nginx-access.json")
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

    # write updated statistic file:
    with open(args.statfile, "w") as sf:
       json.dump(d,sf)  
    return 0

if __name__ == "__main__":
    runws()

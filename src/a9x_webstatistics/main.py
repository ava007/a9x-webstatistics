import argparse
import io
import json
import re
import sys
from datetime import datetime
from .updatestatistics import upd
from .updateStatisticsV0001 import updV0001
from .summarizemonth import summonth
from .summarizemonthV0001 import sumMonthV0001
from .migratev0001 import migv0001
from importlib.metadata import version
import geoip2.database

def parseRec(rec, log_pattern, j, georeader):
    #print(str(rec))
    j['records_read_total'] += 1

    r = {}
    # skip comments recs
    if rec[0:1] == '#':
        j['records_skipped_comment'] += 1
        return r,j

    data = re.search(log_pattern, rec)
    print("parseRec Data: " + str(data))
    if data:
        datadict = data.groupdict()
        ip_address = datadict["ipaddress"]
        timestamp = datadict["dateandtime"]
        request = datadict["url"]
        bytes_sent = datadict["bytessent"]
        referer = datadict["referer"]
        user_agent = datadict["useragent"]
        status = datadict["statuscode"]
        method = datadict["method"]
        j['records_processed_for_statistic'] += 1
        try:
            grrsp = georeader.country(ip_address)
            country = grrsp.country.name
        except geoip2.errors.AddressNotFoundError:
            country = None
        
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
        if country:
            r['country'] = country
    
    return r,j


def runws(statfile, infile, geoip, verbosity, domain):

    try: 
        georeader = geoip2.database.Reader(geoip)
    except FileNotFoundError:
        print("geoip2 file not found, continue processing")

    # init statistic file if it does not exist:
    d = {}
    d['timelastrec'] = '19991231235959'
    d['days'] = {}
    #d['v0001'] = {}
    #d['v0001']['days'] = {}

    # init job results
    j = {
        'records_read_total': 0,
        'records_skipped_comment': 0,
        'records_already_processed': 0,
        'records_processed_for_statistic': 0,
    }
    
    # load statistic file if it exists
    try:
        f = open(statfile) 
        d = json.load(f) 
    except FileNotFoundError:   # first call: file does not exists
        print("-s statistic file not found, it will be automatically created")
    except json.JSONDecodeError:
        print("-s json file is not valid")

    visitIP = {}
    lasttimerecobj = datetime.strptime(d['timelastrec'],"%Y%m%d%H%M%S")
    print("lasttimerecobj: " + str(lasttimerecobj))

    log_pattern = re.compile(
        r"""
        (?P<ipaddress>
        \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|               # ipv4
        (                                                  
        ([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|          # ipv6 1:2:3:4:5:6:7:8
        ([0-9a-fA-F]{1,4}:){1,7}:|                         # ipv6 1::              1:2:3:4:5:6:7::
        ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|         # ipv6 1::8             1:2:3:4:5:6::8  1:2:3:4:5:6::8
        ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|  # ipv6 1::7:8           1:2:3:4:5::7:8  1:2:3:4:5::8
        ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|  # ipv6 1::6:7:8         1:2:3:4::6:7:8  1:2:3:4::8
        ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|  # ipv6 1::5:6:7:8       1:2:3::5:6:7:8  1:2:3::8
        ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|  # ipv6 1::4:5:6:7:8     1:2::4:5:6:7:8  1:2::8
        [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|       # ipv6 1::3:4:5:6:7:8   1::3:4:5:6:7:8  1::8  
        :((:[0-9a-fA-F]{1,4}){1,7}|:)|                     # ipv6 ::2:3:4:5:6:7:8  ::2:3:4:5:6:7:8 ::8       ::     
        fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|     # fe80::7:8%eth0   fe80::7:8%1  (link-local IPv6 addresses with zone index)
        ::(ffff(:0{1,4}){0,1}:){0,1}
        ((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}
        (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|          # ::255.255.255.255   ::ffff:255.255.255.255  ::ffff:0:255.255.255.255  (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
        ([0-9a-fA-F]{1,4}:){1,4}:
        ((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}
        (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])           # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
        )
        )[ ]-[ ]-[ ]\[(?P<dateandtime>\d{2}\/[a-zA-Z]{3}\/\d{4}:\d{2}:\d{2}:\d{2}[ ](\+|\-)\d{4})\][ ]
        ((?P<method>)(\"(GET|POST|HEAD|PUT|DELETE|OPTIONS|PROPFIND))[ ]
        (?P<url>.+)[ ](HTTP\/(1\.1|2\.0)"))[ ]
        (?P<statuscode>\d{3})[ ]
        (?P<bytessent>\d+)[ ]
        (["](?P<referer>[^"]+)["])[ ]
        (["](?P<useragent>[^"]+)["])
        """,
        flags=re.VERBOSE
    )
    
    # process infile:
    with open(infile,'r') as infile:
        for rec in infile:
            recparsed, j = parseRec(rec, log_pattern, j, georeader)
            # skip unrecognized records:
            if not recparsed or recparsed['timestamp'] is None or recparsed['ip'] is None:
                continue
            # skip already processed data:
            if recparsed['timestamp']  <=  d['timelastrec']:
                j['records_already_processed'] += 1
                continue
            d, visitIP = upd(d, recparsed, visitIP, domain)
            d, visitIP = updV0001(d, recparsed, visitIP, domain)
            j['records_processed_for_statistic'] += 1
            

    # summarize previous months
    d = summonth(d)
    
    # write updated statistic file:
    with open(statfile, "w") as sf:
       json.dump(d,sf)  

    d = sumMonthV0001(d, statfile)

    print("Rec processed: " + str(j['records_processed_for_statistic']))
    print("Reco skipped: " +  str(j['records_already_processed']))
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False,
        prog='a9x_webstatistics',
        epilog="Version: "+ version('a9x-webstatistics')
    )
    parser.add_argument("-s", "--statfile", help="json file that contains calculated statistics", default="webstat.json")
    parser.add_argument("-i", "--infile", help="filename including path to web server access log that contains input data", default="nginx_access.log")
    parser.add_argument("-g", "--geoip", help="path to GeoIP2-Country.mmdb file", default="GeoIP2-Country.mmdb")
    parser.add_argument("-v", "--verbose", help="increase output verbosity, 0=none, 1=increased verbosity", default="0")
    parser.add_argument("-d", "--domain", help="domain https://logikfabrik.com on which the access log file runs", default="https://logikfabrik.com")
    args, unknown = parser.parse_known_args()

    migv0001(statfile=args.statfile)
    runws(statfile=args.statfile, infile=args.infile, geoip=args.geoip, verbosity=args.verbose, domain=args.domain)

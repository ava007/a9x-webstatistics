# -*- coding: utf-8 -*-
import io, ipaddress, sys, argparse, json, ast
from operator import itemgetter
from copy import deepcopy
from importlib.metadata import version
from datetime import datetime, timedelta
from a9x_webstatistics import __version__
from .gencockpitsubV0001 import *
    
def runGenCockpitV0001(infile, outfile, verbosity, domain, omit, efeature):

    owndomain = domain.replace('http://','')
    owndomain = owndomain.replace('https://','')
    owndomain = owndomain.replace('www.','')
    
    with open(infile) as json_file:
        d = json.load(json_file) 
        
        h = genHeader(owndomain)
        h += "\n" + '<div class="row pt-3"><div class="col-12">'
        h += '<h1>Webstatistics for ' + owndomain + '</h1>'
        h += '<a href="#hdDay" class="btn btn-primary me-3" role="button" data-bs-toggle="button">Daily Statistics</a>'
        h += '<a href="#hdLongTherm" class="btn btn-primary me-3" role="button" data-bs-toggle="button">Long Therm Statistics</a>'
        h += '</div></div>'
        h += "\n" + '<div class="row pt-4"><div class="col-12">'
        h += '<h2 id="hdDay">Daily statistics for ' + owndomain + '</h2>'
        h += "<p><small>Last record included in statistic: <script>document.write(DT2Locale('" + d['timelastrec'] + "'));</script></small></p>"
        h += '</div></div>'

        h += "\n" + '<div class="row pt-4">' + dailyHitsVisitsChart(d, owndomain, omit) + '</div>' + "\n"

        h += "\n" + '<div class="row pt-4">' + navChord(d, owndomain, omit) + '</div>' + "\n"

        # lastDate is the youngest date in the json
        # firstDate is the oldest date in the json

        lastDate = sorted(list(d["v0001"]["days"].keys() ))[-1]
        if verbosity == '99':
            print("gencockpit: lastDate (youngest) from json:" + str(lastDate) )
        if len(lastDate) >= 6:
            actYearMonth = lastDate[0:6]
        else:
            actYearMonth = lastDate[0:4] + '12'
            lastDate = lastDate[0:4] + '1231'

        firstDate = sorted(list(d["v0001"]["days"].keys() ))[0]
        if verbosity == '99':
            print("gencockpit: firstDate (oldest) from json:" + str(firstDate) )
        if len(firstDate) == 6:
            firstDate += '01'   # add day to YYYYMM
        if len(firstDate) == 4:
            firstDate += '0101'   # add MonthDay to YYYY
        d1 = datetime.strptime(firstDate, "%Y%m%d")
        
        if len(lastDate) == 6:
            if lastDate[4:6] == '02':
                lastDate += '28'   # add day to YYYYMM
            else:
                lastDate += '30'   # add day to YYYYMM
        if len(lastDate) == 4:
            lastDate += '1231'   # add MonthDay to YYYY
        d2 = datetime.strptime(lastDate, "%Y%m%d")

        # difference between dates in timedelta
        deltaInDays = d2 - d1
        if verbosity == '99':
            print("gencockpit: firstDate:" + str(firstDate) + " lastDate: " + str(lastDate) )
            print(f'Difference is {deltaInDays.days} days')

        # row for top domains and urls:
        h += "\n" + '<div class="row pt-4">'
        h += dailyTopDomains(d, owndomain, omit)
        h += dailyTopUrl(d, owndomain, omit)
        h += dailyTopCountries(d, owndomain, omit)
        h += '</div>'

        # accepted languages by browser:
        h += "\n" + '<div class="row pt-4">' + cockpitLanguages(d, owndomain) + '</div>' + "\n"

        # cache, response_time:
        h += "\n" + '<div class="row pt-4">' + performance(d) + '</div>'

        # quality:
        h += "\n" + '<div class="row pt-4">' + dailyQuality(d, owndomain, omit, verbosity) + '</div>'
        

        # show long term not on first runs:
        if deltaInDays.days > 32:

            h += "\n" + '<h2 id="hdLongTerm" class="pt-4">Long Term Statistics for ' + owndomain + '</h2>'
        
            h += "\n" + '<div class="row pt-4">' + monthlyHitsVisitsChart(d, owndomain, omit, verbosity) +  "\n"
            h +=  monthlyTopDomains(d, owndomain, omit) + '</div>' + "\n"
        
            h += "\n" + '<div class="row pt-4">' + monthlyTopUrl(d, owndomain, omit, verbosity) + "\n"
            h += monthlyTopCountries(d, owndomain, omit) + '</div>' + "\n"

            h += "\n" + '<div class="row pt-4">' + navChordLongterm(d, owndomain, omit) + '</div>' + "\n"
 
        h += "\n" + '<footer class="row bg-light py-4 mt-4">'
        h += '<div class="col"><h2>About</h2>'
        h += '<ul class="nav flex-column">'
        h += '<li class="nav-item mb-2"><a href="https://github.com/ava007/a9x-webstatistics" class="nav-link p-0 text-body-secondary">© 2024-2026 a9x-webstatistics</a></li>'
        h += '<li class="nav-item mb-2">' + __version__ + '</li>'
        h += '<li class="nav-item mb-2">salvo errore et omissione</li>'
        h += '</ul></div>' + "\n"

        h += '<div class="col"><h2>Sponsored by</h2>'
        h += '<ul class="nav flex-column">'
        h += '<li class="nav-item mb-2"><a href="https://www.logikfabrik.com" class="nav-link p-0 text-body-secondary">LogikFabrik.com - Knowledge Management</a></li>'
        h += '<li class="nav-item mb-2"><a href="https://www.logikfabrik.com/aboutwebstats.html" class="nav-link p-0 text-body-secondary">Live Examples</a></li>'
        h += '</ul></div>' + "\n"
          
        h += '<div class="col"><h2>Abbreviations</h2>'
        h += '<ul class="nav flex-column">'
        h += '<li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">Hit: Download request of a html file</a></li>'
        h += '<li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">URL: Uniform Resource Locator</a></li>'
        h += '</ul></div>' + "\n"

        h += '</footer>'

        h += '</div>'  # end of class "container"
        h += '</body></html>'

        # write html to file:
        outfile = open(outfile, "w")
        outfile.write(h)
        outfile.close()

        return 0
        
def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False,
        prog='a9x_webstatistics',
        epilog="Version: "+ version('a9x-webstatistics')
    )
    parser.add_argument("-i", "--infile", help="json file that contains calculated statistics", default="webstat.json")
    parser.add_argument("-o", "--outfile", help="html file that contains html cockpit", default="webstat.html")
    parser.add_argument("-d", "--domain", help="domain https://logikfabrik.com on which the access log file runs", default="https://logikfabrik.com")
    parser.add_argument("-t", "--omit", help="omits path ie. will not display these path in generated cockpit", action="append")
    parser.add_argument("-v", "--verbose", help="increase output verbosity, 0=none, 1=increased verbosity", default="0")
    parser.add_argument("-ef", "--efeature", help="use experimentalfeature number, 0=none, 1-99=feature", default="0")
    args, unknown = parser.parse_known_args()

    if args.omit is None:
        args.omit = []        

    runGenCockpitV0001(infile=args.infile, outfile=args.outfile, verbosity=args.verbose, domain=args.domain, omit=args.omit, efeature=args.efeature)

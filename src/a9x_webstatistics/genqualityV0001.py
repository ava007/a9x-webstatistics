# -*- coding: utf-8 -*-
import io, ipaddress, sys, argparse, json, ast
from operator import itemgetter
from copy import deepcopy
from importlib.metadata import version
from datetime import datetime, timedelta
from a9x_webstatistics import __version__
from .gencockpitsubV0001 import *
    
def runGenQualityV0001(infile, outfile, verbosity, domain, omit, efeature):

    owndomain = domain.replace('http://','')
    owndomain = owndomain.replace('https://','')
    owndomain = owndomain.replace('www.','')
    
    with open(infile) as json_file:
        d = json.load(json_file) 
        
        h = genHeader(owndomain)
        h += "\n" + '<div class="row pt-3"><div class="col-12">'
        h += '<h1>Quality Reportings for ' + owndomain + '</h1>'
        h += '<a href="#hdDay" class="btn btn-primary me-3" role="button" data-bs-toggle="button">Daily Statistics</a>'
        h += '<a href="#hdMonth" class="btn btn-primary me-3" role="button" data-bs-toggle="button">Monthly Statistics</a>'
        h += '<a href="#hdYear" class="btn btn-primary" role="button" data-bs-toggle="button">Yearly Statistics</a>'
        h += '</div></div>'
        h += "\n" + '<div class="row pt-4"><div class="col-12">'
        h += '<h2 id="hdDay">Daily statistics for ' + owndomain + '</h2>'
        h += "<p><small>Last record included in statistic: <script>document.write(DT2Locale('" + d['timelastrec'] + "'));</script></small></p>"
        h += '</div></div>'

        h += '<div class="row pt-4">' + dailyHitsVisitsChart(d, owndomain, omit) + '</div>' + "\n"

        h += '<div class="row pt-4">' + navChord(d, owndomain, omit) + '</div>' + "\n"
        
        lastDate = list(d['v0001']['days'].keys())[-1]
        actYearMonth = lastDate[0:6]

        firstDate = list(d['v0001']['days'].keys())[0]
        
        # row for top domains and urls:
        h += '<div class="row pt-4">'
        h += dailyTopDomains(d, owndomain, omit)
        h += dailyTopUrl(d, owndomain, omit)
        h += dailyTopCountries(d, owndomain, omit)
        h += '</div>'

        # accepted languages by browser:
        h += '<div class="row pt-4">' + cockpitLanguages(d, owndomain) + '</div>' + "\n"

        # cache, response_time:
        h += '<div class="row pt-4">' + performance(d) + '</div>'
       
        # top external landings (friends):
        #h += '<div class="row pt-4">' + externalFriends(d, owndomain, omit) + '</div>'  + "\n"

        if len(firstDate) == 6:
            firstDate += '01'   # add day to YYYYMM
        d1 = datetime.strptime(firstDate, "%Y%m%d")
        d2 = datetime.strptime(lastDate, "%Y%m%d")

        # difference between dates in timedelta
        deltaInDays = d2 - d1
        #print(f'Difference is {deltaInDays.days} days')

        # show long term not on first runs:
        if deltaInDays.days > 32:

            h += '<h2 id="LongTerm" class="pt-4">Long Term Statistics for ' + owndomain + '</h2>'
        
            h += '<div class="row pt-4">' + monthlyHitsVisitsChart(d, owndomain, omit) +  "\n"
            h +=  monthlyTopDomains(d, owndomain, omit) + '</div>' + "\n"
        
            h += '<div class="row pt-4">' + monthlyTopUrl(d, owndomain, omit, verbosity) + "\n"
            h += monthlyTopCountries(d, owndomain, omit) + '</div>' + "\n"

            h += '<div class="row pt-4">' + navChordLongterm(d, owndomain, omit) + '</div>' + "\n"

        tquality = {}   # nested dictionary!
        for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            curYearMonth = k[0:6]
            if curYearMonth == actYearMonth:
                if 'quality' in d['v0001']['days'][k]:
                    for sk,sv in d['v0001']['days'][k]['quality'].items():
                        #print('sk: ' + str(sk) + ' sv: ' + str(sv))
                        if sk not in tquality:
                            tquality[sk] = {}
                            tquality[sk]['count'] = 1
                            tquality[sk]['status'] = sv['status']
                            tquality[sk]['from'] = sv['from']
                            tquality[sk]['comment'] = sv['comment']
                            tquality[sk]['lastoccured'] = k
                        else:
                            tquality[sk]['count']  += 1

        if len(tquality) > 0:
            h += '<div class="row pt-4">' 
            h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
            h += '<div class="card mt-2"><div class="card-body">'
            h += '<h3 class="card-title">Quality Improvements</h3>'
            h += '<p class="card-text">Quality improvements that should be implemented:</p>'
            h += '<table class="table-responsive text-break"><thead><tr><th scope="col">Status</th><th scope="col">affected URL</th><th scope="col">Count</th><th scope="col">Remark</th><th scope="col">Date last occured</th></tr></thead>'
            i = 0
            for k, v in sorted(tquality.items(), key=lambda x: (x[1]['lastoccured']), reverse=True):
                h += '<tr><td>' + str(v['status']) + '</td><td>' + str(k) + "</td>" 
                h += '<td style="text-align: right">' + str(format(v['count'],',')) + '</td>'
                h += '<td>' + v['comment'] + '</td>'
                h += "<td><script>document.write(DT2Locale('" + v['lastoccured'] + "'));</script></td>"
                h += '</tr>'
                if len(v['from']) > 1:
                    h += '<tr><td></td><td colspan="4">called by: ' + v['from'] + '</td></tr>'
                i += 1
                if i == 10:
                    break
            h += '</table>'
            h += '</div></div></div></div>' + "\n\n"   # end of card and col
 
        h += '<footer class="row bg-light py-4 mt-4">'
        h += '<div class="col"><h2>About</h2>'
        h += '<ul class="nav flex-column">'
        h += '<li class="nav-item mb-2"><a href="https://github.com/ava007/a9x-webstatistics" class="nav-link p-0 text-body-secondary">© 2024-2025 a9x-webstatistics</a></li>'
        h += '<li class="nav-item mb-2">' + __version__ + '</li>'
        h += '<li class="nav-item mb-2">salvo errore et omissione</li>'
        h += '</ul></div>' + "\n"

        h += '<div class="col"><h2>Sponsored by</h2>'
        h += '<ul class="nav flex-column">'
        h += '<li class="nav-item mb-2"><a href="https://www.logikfabrik.com/aboutwebstats.html" class="nav-link p-0 text-body-secondary">LogikFabrik.com</a></li>'
        h += '<li class="nav-item mb-2"><a href="https://www.logikfabrik.com/aboutwebstats.html" class="nav-link p-0 text-body-secondary">Live Example</a></li>'
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

    runGenQualityV0001(infile=args.infile, outfile=args.outfile, verbosity=args.verbose, domain=args.domain, omit=args.omit, efeature=args.efeature)

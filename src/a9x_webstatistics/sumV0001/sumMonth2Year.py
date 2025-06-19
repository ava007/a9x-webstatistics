from copy import deepcopy
from datetime import datetime, timedelta
from operator import itemgetter
import json

def sumMonth2YearV0001(d, statfile, verbosity):
    
    # accumulate months to year:
    # if lasttimerec is 2025xxxx then summup to (inkl) 202212

    yearInt = int(d['timelastrec'][0:4])
    yearInt = yearInt - 3
    sumUntilMonth = str(yearInt) + '12'
   
    lasttimerecobj = datetime.strptime(d['timelastrec'],"%Y%m%d%H%M%S")
    print("sumMonth2Year:  sumup inkl: " + sumUntilMonth + "  lasttimerecobj: " + d['timelastrec'])

    dtmp = deepcopy(d)
    for x in dtmp['v0001']['days']:
        # skip days, years
        if len(x) != 6:  
            continue
        # skip young month:
        if x > sumUntilMonth:
            continue
            
        # here onward: sum up
        recYear = x[0:4]  # [start:end] index 0 to index 4 (end not inclusive)
        if recYear not in d['v0001']['days']:
            d['v0001']['days'][recYear] = {}
            d['v0001']['days'][recYear]['user'] = {}
            d['v0001']['days'][recYear]['user']['visits'] = 0;
            d['v0001']['days'][recYear]['user']['bytesSent']   = 0;
            d['v0001']['days'][recYear]['user']['countryHits'] = {}
            d['v0001']['days'][recYear]['user']['deviceHits'] = {}
            d['v0001']['days'][recYear]['user']['deviceHits']['mobile']  = 0 
            d['v0001']['days'][recYear]['user']['deviceHits']['tablet']  = 0 
            d['v0001']['days'][recYear]['user']['deviceHits']['desktop'] = 0 
            d['v0001']['days'][recYear]['user']['serverResponseCode'] = {}
            d['v0001']['days'][recYear]['user']['countryHits'] = {}
            d['v0001']['days'][recYear]['user']['topUrl'] = {}
            d['v0001']['days'][recYear]['user']['language'] = {}
            d['v0001']['days'][recYear]['robot'] = {};
            d['v0001']['days'][recYear]['robot']['bytesSent']   = 0;
            d['v0001']['days'][recYear]['robot']['robotHits'] = 0
            d['v0001']['days'][recYear]['robot']['serverResponseCode'] = {}

        if 'visits' in dtmp['v0001']['days'][x]['user']:
            d['v0001']['days'][recYear]['user']['visits'] += dtmp['v0001']['days'][x]['user']['visits']
        if 'bytesSent' in dtmp['v0001']['days'][x]['user']:
            d['v0001']['days'][recYear]['user']['bytesSent']  += int(dtmp['v0001']['days'][x]['user']['bytesSent'])

        if 'countryHits' in dtmp['v0001']['days'][x]['user']:
            for ck, cv in sorted(dtmp['v0001']['days'][x]['user']['countryHits'].items(), key=itemgetter(1), reverse=True):
                if ck in d['v0001']['days'][recYear]['user']['countryHits']:
                    d['v0001']['days'][recYear]['user']['countryHits'][ck] += cv
                else:
                    d['v0001']['days'][recYear]['user']['countryHits'][ck] = cv

        if 'deviceHits' in  dtmp['v0001']['days'][x]['user']:   
            d['v0001']['days'][recYear]['user']['deviceHits']['mobile']  += dtmp['v0001']['days'][x]['user']['deviceHits']['mobile']
            d['v0001']['days'][recYear]['user']['deviceHits']['tablet']  += dtmp['v0001']['days'][x]['user']['deviceHits']['tablet']
            d['v0001']['days'][recYear]['user']['deviceHits']['desktop'] += dtmp['v0001']['days'][x]['user']['deviceHits']['desktop']
        
        # Server Response Code:
        if 'serverResponseCode' in dtmp['v0001']['days'][x]['user']:
            for ck,cv in dtmp['v0001']['days'][x]['user']['serverResponseCode'].items():
                print("sumMonth2Year Responsecode In:  " + ck + ": " + str(cv) )
          
                if ck in d['v0001']['days'][recYear]['user']['serverResponseCode']:
                    d['v0001']['days'][recYear]['user']['serverResponseCode'][ck] += cv
                else:
                    d['v0001']['days'][recYear]['user']['serverResponseCode'][ck] = cv
                print("sumMonth2Year ResponseCode Out: " + str(d['v0001']['days'][recYear]['user']['serverResponseCode']))
        
        # Country Hits
        if 'countryHits' in dtmp['v0001']['days'][x]['user']:
            for ck,cv in dtmp['v0001']['days'][x]['user']['countryHits'].items():
                print("sumMonth2Year In: " + str(x) + " country: " + ck + ": " + str(cv) )
                if ck in d['v0001']['days'][recYear]['user']['countryHits']:
                    d['v0001']['days'][recYear]['user']['countryHits'][ck] += cv
                else:
                    d['v0001']['days'][recYear]['user']['countryHits'][ck] = cv
            print("sumMonth2Year Out: " + str(recYear) + ": " + str(d['v0001']['days'][recYear]['user']['countryHits']) )


        # Top URLs:
        if 'topUrl' in dtmp['v0001']['days'][x]['user']:
            for ck,cv in dtmp['v0001']['days'][x]['user']['topUrl'].items():
                print("sumMonth2Year In: " + str(x) + " topurl: " + ck + ": " + str(cv) )
                if ck in d['v0001']['days'][recYear]['user']['topUrl']:
                    d['v0001']['days'][recYear]['user']['topUrl'][ck] += cv
                else:
                    d['v0001']['days'][recYear]['user']['topUrl'][ck] = cv
            print("sumMonth2Year Out: " + str(recYear) + ": " + str(d['v0001']['days'][recYear]['user']['topUrl']))

        # nav   - nav is stored on the last day of month
        if 'nav' in dtmp['v0001']['days'][x]['user']:
            if 'nav' not in d['v0001']['days'][recYear]['user']:
                d['v0001']['days'][recYear]['user']['nav'] = []
            # take to top 20 external:
            cnt = 0
            for e in sorted(dtmp['v0001']['days'][x]['user']['nav'], key=itemgetter('c'), reverse=True):
                if 'p' not in e or e['p'] != 'e':  # not external nav
                    continue
                # if source/target exists: increment count, else append:
                found = False
                for f in d['v0001']['days'][recYear]['user']['nav']:            
                    if (e['s'] == f['s']
                        and e['t'] == f['t']):
                        f['c'] += e['c']
                        found = True
                        if verbosity == "99":
                            print('sumMonth2Year: nav: ' + str(x) + ': ' + str(e) + " added to existing - external")
                        break
                if found == False:
                    d['v0001']['days'][recYear]['user']['nav'].append(e)
                    cnt += 1
                    if verbosity == "99":
                        print('sumMonth2Year: nav: ' + str(x) + ': ' + str(e) + " appended - external")
                if cnt > 20:
                    break

            # take up to top 50 internal:
            cnt = 0
            for e in sorted(dtmp['v0001']['days'][x]['user']['nav'], key=itemgetter('c'), reverse=True):
                if 'p' in e and e['p'] == 'e':  # omit external
                    continue
                if verbosity == "99":
                    print('sumMonth2YearV0001: nav: ' + str(x) + ': ' + str(e))
                # if source/target exists: increment count, else append:
                found = False
                for f in d['v0001']['days'][recYear]['user']['nav']:            
                    if (e['s'] == f['s']
                        and e['t'] == f['t']):
                        f['c'] += e['c']
                        found = True
                        if verbosity == "99":
                            print('sumMonth2Year: nav: ' + str(x) + ': ' + str(e) + " added to existing - internal")
                        break
                if found == False:
                    d['v0001']['days'][recYear]['user']['nav'].append(e)
                    cnt += 1
                    if verbosity == "99":
                        print('sumMonth2Year: nav: ' + str(x) + ': ' + str(e) + " appended - internal")
                if cnt > 50:
                    break
        
        # languages:
        if 'language' in dtmp['v0001']['days'][x]['user']:
            for ck,cv in dtmp['v0001']['days'][x]['user']['language'].items():
                print("sumMonth2Year In: " + str(x) + " language: " + ck + ": " + str(cv) )
                if ck in d['v0001']['days'][recYear]['user']['language']:
                    d['v0001']['days'][recYear]['user']['language'][ck] += cv
                else:
                    d['v0001']['days'][recYear]['user']['language'][ck] = cv
            print("sumMonth2Year Out: " + str(recYear) + ": " + str(d['v0001']['days'][recYear]['user']['language']))

        # Robots
        if 'robotHits' in dtmp['v0001']['days'][x]['robot']:
            d['v0001']['days'][recYear]['robot']['robotHits'] += dtmp['v0001']['days'][x]['robot']['robotHits']
        if 'bytesSent' in dtmp['v0001']['days'][x]['robot']:
            d['v0001']['days'][recYear]['robot']['bytesSent']  += int(dtmp['v0001']['days'][x]['robot']['bytesSent'])

        # Robot Server Response Code:
        if 'serverResponseCode' in dtmp['v0001']['days'][x]['robot']:
            for ck,cv in dtmp['v0001']['days'][x]['robot']['serverResponseCode'].items():
                print("sumMonth2Year:  Responsecode  In Robot: " + ck + ": " + str(cv) )
                if ck in d['v0001']['days'][recYear]['robot']['serverResponseCode']:
                    d['v0001']['days'][recYear]['robot']['serverResponseCode'][ck] += cv
                else:
                    d['v0001']['days'][recYear]['robot']['serverResponseCode'][ck] = cv
                print("sumMonth2Year responseCode Out Robot: " + str(d['v0001']['days'][recYear]['robot']['serverResponseCode']))

                    
        # delete obsolete data:
        del d['v0001']['days'][x]
        if verbosity == '99':
             print("sumMonth2Year Result: " + str(recYear) + ": " + str( d['v0001']['days'][recYear] ))

    return d

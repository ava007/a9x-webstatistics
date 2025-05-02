from copy import deepcopy
from datetime import datetime, timedelta
from operator import itemgetter
import json

def sumMonth2YearV0001(d, statfile):
    
    # accumulate months to year:
    # if lasttimerec is 2025xxxx then summup to (inkl) 202212

    yearInt = int(d['timelastrec'][0:4])
    yearInt = yearInt - 3
    print("sumMonth2Year:  year of last rec: " + str(yearInt) + ",  accumulate till (including): " + str(yearInt))

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
                print("sumMonth2Year:  Responsecode  In: " + ck + ": " + str(cv) )
          
                if ck in d['v0001']['days'][recYear]['user']['serverResponseCode']:
                    d['v0001']['days'][recYear]['user']['serverResponseCode'][ck] += cv
                else:
                    d['v0001']['days'][recYear]['user']['serverResponseCode'][ck] = cv
                print("sumMonth2Year responseCode Out: " + str(d['v0001']['days'][recYear]['user']['serverResponseCode']))
        
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

    return d

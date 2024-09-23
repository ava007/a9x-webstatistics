from copy import deepcopy
from datetime import datetime, timedelta
from operator import itemgetter
import json

def sumMonthV0001(d, statfile):
    
    # accumulate previous months:
    # 2024.08.02 => 2024.06
    # 2024.08.30 => 2024.06
    # 2024.08.31 => 2024.07

    sumUntilDay = datetime.now() - timedelta(days=62)
    sumTill = sumUntilDay.strftime("%Y%m")
    print("sumMonthV0001: accumulate including month: "  + sumTill)   # 202312
    
    # iterate over days to accumulate months:
    dtmp = deepcopy(d)
    for x in dtmp['v0001']['days']:
        # if date has a day:
        if len(x) > 6:
            recMonth = x[0:6]
            if recMonth <= sumTill:
                #print("sumMonthV0001: recMonth : " + recMonth + "  day x: " + x)
                if recMonth not in d['v0001']['days']:
                            
                    d['v0001']['days'][recMonth] = {}
                    d['v0001']['days'][recMonth]['user'] = {}
                    d['v0001']['days'][recMonth]['user']['visits'] = 0;
                    d['v0001']['days'][recMonth]['user']['bytesSent']   = 0;
                    d['v0001']['days'][recMonth]['user']['countryHits'] = {}
                    d['v0001']['days'][recMonth]['user']['deviceHits'] = {}
                    d['v0001']['days'][recMonth]['user']['deviceHits']['mobile']  = 0 
                    d['v0001']['days'][recMonth]['user']['deviceHits']['tablet']  = 0 
                    d['v0001']['days'][recMonth]['user']['deviceHits']['desktop'] = 0 

                    d['v0001']['days'][recMonth]['user']['externalFriendHits'] = {}
                    d['v0001']['days'][recMonth]['user']['topUrl'] = {}
                    d['v0001']['days'][recMonth]['user']['serverResponseCode'] = {}
                    d['v0001']['days'][recMonth]['robot'] = {}
                    d['v0001']['days'][recMonth]['robot']['bytesSent']   = 0;
                    d['v0001']['days'][recMonth]['robot']['robotHits']   = 0;
                    d['v0001']['days'][recMonth]['quality'] = {}

                # always check, if structure exists as we might start within the month (not on the first day of month)
                if 'visits' in dtmp['v0001']['days'][x]['user']:
                    d['v0001']['days'][recMonth]['user']['visits']     += dtmp['v0001']['days'][x]['user']['visits']
                if 'bytesSent' in dtmp['v0001']['days'][x]['user']:
                    d['v0001']['days'][recMonth]['user']['bytesSent']  += int(dtmp['v0001']['days'][x]['user']['bytesSent'])

                if 'countryHits' in dtmp['v0001']['days'][x]['user']:
                    for ck,cv in dtmp['v0001']['days'][x]['user']['countryHits'].items():
                        #print("sum: country: " + ck + ": " + str(cv) )
                        #print("sum: countries" + str(dtmp['v0001']['days'][recMonth]['user']['countryHits']))
                        if ck in d['v0001']['days'][recMonth]['user']['countryHits']:
                            d['v0001']['days'][recMonth]['user']['countryHits'][ck] += cv
                        else:
                            d['v0001']['days'][recMonth]['user']['countryHits'][ck] = cv;
                
                if 'deviceHits' in  dtmp['v0001']['days'][x]['user']:   
                    d['v0001']['days'][recMonth]['user']['deviceHits']['mobile']  += dtmp['v0001']['days'][x]['user']['deviceHits']['mobile']
                    d['v0001']['days'][recMonth]['user']['deviceHits']['tablet']  += dtmp['v0001']['days'][x]['user']['deviceHits']['tablet']
                    d['v0001']['days'][recMonth]['user']['deviceHits']['desktop'] += dtmp['v0001']['days'][x]['user']['deviceHits']['desktop']
                
                # external sources:
                if 'externalFriendHits' in dtmp['v0001']['days'][x]['user']:
                    for ck,cv in dtmp['v0001']['days'][x]['user']['externalFriendHits'].items():
                        #print("sum: externalFriendHits: " + ck + ": " + str(cv) )

                        #print("sum extFriendHits: " + str(d['v0001']['days'][recMonth]['user']['externalFriendHits']))
                        if ck in d['v0001']['days'][x]['user']['externalFriendHits']:
                            d['v0001']['days'][recMonth]['user']['externalFriendHits'][ck] += cv
                        else:
                            d['v0001']['days'][recMonth]['user']['externalFriendHits'][ck] = cv;
                
                if 'robot' in dtmp['v0001']['days'][x]:
                    if 'robotHits' in dtmp['v0001']['days'][x]['robot']:
                        d['v0001']['days'][recMonth]['robot']['robotHits'] += dtmp['v0001']['days'][x]['robot']['robotHits']
                    if 'bytesSent' in dtmp['v0001']['days'][x]['robot']:
                        d['v0001']['days'][recMonth]['robot']['bytesSent'] += int(dtmp['v0001']['days'][x]['robot']['bytesSent'])


                # Server Response Code:
                if 'serverResponseCode' in dtmp['v0001']['days'][x]['user']:
                    for ck,cv in dtmp['v0001']['days'][x]['user']['serverResponseCode'].items():
                        #print("sumV0001:  Responsecode: " + ck + ": " + str(cv) )

                        #print("sumV0001 responseCode: " + str(d['v0001']['days'][recMonth]['user']['serverResponseCode']))
                        if ck in d['v0001']['days'][recMonth]['user']['serverResponseCode']:
                            d['v0001']['days'][recMonth]['user']['serverResponseCode'][ck] += cv
                        else:
                            d['v0001']['days'][recMonth]['user']['serverResponseCode'][ck] = cv;

                # topurl:
                if 'topUrl' in dtmp['v0001']['days'][x]['user']:
                    for ck,cv in dtmp['v0001']['days'][x]['user']['topUrl'].items():
                        #print("sum: topurl: " + ck + ": " + str(cv) )   
                        # sum: topurl: /kl/view/325fbfbf-cf58-400e-abc4-4173e7b015e4/: 2

                        #print("sum topurl: " + str(d['v0001']['days'][recMonth]['user']['topUrl']))
                        # sum topurl: {'/kl/view/f95c0c51-5f00-42f6-ae4c-50abb30ed665/': 2,
                        #              '/kl/view/973a9773-2f06-4f8c-a4b6-ac785b96c990/' : 1,
                        
                        if ck in d['v0001']['days'][recMonth]['user']['topUrl']:
                            d['v0001']['days'][recMonth]['user']['topUrl'][ck] += cv
                        else:
                            d['v0001']['days'][recMonth]['user']['topUrl'][ck] = cv;
                            
                # quality:
                if 'quality' in dtmp['v0001']['days'][x]:
                    for ck,cv in dtmp['v0001']['days'][x]['quality'].items():
                        if ck in d['v0001']['days'][recMonth]['quality']:
                            d['v0001']['days'][recMonth]['quality'][ck]['count'] += 1
                        else:
                            d['v0001']['days'][recMonth]['quality'][ck] = cv

                # navigation on the first day of the month:  take the 24 path with the most traffic:
                dayOfMonth = x[-2:]
                if 'navigation' in dtmp['v0001']['days'][x]['user'] and dayOfMonth == '01':
                    d['v0001']['days'][recMonth]['user']['navigation'] = {}
                    pcount = 0
                    for nk, nv in sorted(dtmp['v0001']['days'][x]['user']['navigation'].items(), key=itemgetter(1), reverse=True):
                        if nk[0:7] == 'https://':
                            continue
                        if nk[0:6] == 'http://':
                            continue
                            
                        d['v0001']['days'][recMonth]['user']['navigation'][nk] = nv
                        pcount += 1
                        if pcount > 24:
                            break
                        
                del d['v0001']['days'][x]

    # compress by month
    for x in d['v0001']['days']:
        if len(x) == 6:
            if 'countryHits' in d['v0001']['days'][x]['user']:
                tmpCountryHits = dict(sorted(d['v0001']['days'][x]['user']['countryHits'].items(), key=lambda item: item[1], reverse=True))
                i = 0
                d['v0001']['days'][x]['user']['countryHits'] = {}
                for k,v in tmpCountryHits.items():
                    i += 1
                    if i >= 24:
                        break
                    d['v0001']['days'][x]['user']['countryHits'][k] = v
                del tmpCountryHits
                
            # take only 24 TopUrl in a month:
            if 'topUrl' in d['v0001']['days'][x]['user']:
                tmpTopUrl = dict(sorted(d['v0001']['days'][x]['user']['topUrl'].items(), key=lambda item: item[1], reverse=True))
                i = 0
                d['v0001']['days'][x]['user']['topUrl'] = {}
                for k,v in tmpTopUrl.items():
                    i += 1
                    if i >= 24:
                        break
                    d['v0001']['days'][x]['user']['topUrl'][k] = v
                del tmpTopUrl
   
    # write Save - only relevant for testing
    tstat = statfile.replace('.json','v0001sum.json')
    with open(tstat, "w") as sf:
       json.dump(d,sf)
    return d

def compMonthV0001(d):
    # sort accumulated countries              
    for x in d['v0001']['days']:
        if len(x) == 6:
            d['v0001']['days'][x]['user']['countryHits'] = dict(sorted(d['v0001']['days'][x]['user']['countryHits'].items(), key=lambda item: item[1], reverse=True))

        # sort accumulated topurl
        for x in d['v0001']['days']['user']:
            if len(x) == 6:
                 if 'topUrl' in d['v0001']['days'][x]['user']:
                     tmpTopUrl = dict(sorted(d['v0001']['days'][x]['user']['topUrl'].items(), key=lambda item: item[1], reverse=True))
                     i = 0
                     d['v0001']['days'][x]['user']['topUrl'] = {}
                     for k,v in tmpTopUrl.items():
                         i += 1
                         if i >= 24:
                             break
                         d['v0001']['days'][x]['user']['topUrl'][k] = v
                     del tmpTopUrl
    return d

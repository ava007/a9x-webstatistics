from copy import deepcopy
from datetime import datetime, timedelta

def sumMonthV0001(d):
    
    # accumulate previous months:
    # beginning with the 15th day of the month: the previous month can be summarized:
    # 2024.08.31 => 2024.06
    
    sumUntilDay = datetime.now() - timedelta(days=63)
    sumTill = sumUntilDay.strftime("%Y%m")
    print("sumMonthV0001: accumulate including month: "  + sumTill)   # 202312
    
    # iterate over days to accumulate months:
    dtmp = deepcopy(d)
    for x in dtmp['v0001']['days']:
        # if date has a day:
        if len(x) > 6:
            recMonth = x[0:6]
            if recMonth <= sumTill:
                print("sumMonthV0001: recMonth : " + recMonth + "  day x: " + x)
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

                d['v0001']['days'][recMonth]['user']['visits'] += dtmp['v0001']['days'][x]['user']['visits']
                d['v0001']['days'][recMonth]['user']['bytesSent']   += int(dtmp['v0001']['days'][x]['user']['bytesSent'])

                d['v0001']['days'][recMonth]['robot']['robotHits'] += dtmp['v0001']['days'][x]['robot']['visits']
                d['v0001']['days'][recMonth]['robot']['bytesSent']   += int(dtmp['v0001']['days'][x]['robot']['bytesSent'])

                if 'countryHits' in dtmp['v0001']['days'][x]:
                    for ck,cv in dtmp['v0001']['days'][x]['countryHits'].items():
                        print("sum: country: " + ck + ": " + str(cv) )
                        print("sum: countries" + str(d['v0001']['days'][recMonth]['countryHits']))
                        if ck in d['v0001']['days'][recMonth]['countryHits']:
                            d['v0001']['days'][recMonth]['countryHits'][ck] += cv
                        else:
                            d['v0001']['days'][recMonth]['countryHits'][ck] = cv;
                    
                d['v0001']['days'][recMonth]['user']['deviceHits']['mobile']  += d['v0001']['days'][x]['user']['deviceHits']['mobile']
                d['v0001']['days'][recMonth]['user']['deviceHits']['tablet']  += d['v0001']['days'][x]['user']['deviceHits']['tablet']
                d['v0001']['days'][recMonth]['user']['deviceHits']['desktop'] += d['v0001']['days'][x]['user']['deviceHits']['desktop']
                d['v0001']['days'][recMonth]['robot']['robotHits']['others']  += d['v0001']['days'][x]['robot']['robotHits']['others']

                # ANDRE:  hier weiterfahren mit Anpasssungen
                # external sources:
                if 'source' in dtmp['days'][x]:
                    for ck,cv in dtmp['days'][x]['source'].items():
                        print("sum: external Source: " + ck + ": " + str(cv) )

                        print("sum extSource: " + str(d['days'][currMonth]['source']))
                        if ck in d['days'][currMonth]['source']:
                            d['days'][currMonth]['source'][ck] += cv
                        else:
                            d['days'][currMonth]['source'][ck] = cv;

                # Server Response Code:
                for ck,cv in dtmp['days'][x]['serverResponseCode'].items():
                    print("sum:  Responsecode: " + ck + ": " + str(cv) )

                    print("sum responseCode: " + str(d['days'][currMonth]['serverResponseCode']))
                    if ck in d['days'][currMonth]['serverResponseCode']:
                        d['days'][currMonth]['serverResponseCode'][ck] += cv
                    else:
                        d['days'][currMonth]['serverResponseCode'][ck] = cv;

                # topurl:
                if 'topurl' in dtmp['days'][x]:
                    for ck,cv in dtmp['days'][x]['topurl'].items():
                        print("sum: topurl: " + ck + ": " + str(cv) )

                        print("sum topurl: " + str(d['days'][currMonth]['topurl']))
                        if ck in d['days'][currMonth]['topurl']:
                            d['days'][currMonth]['topurl'][ck] += cv
                        else:
                            d['days'][currMonth]['topurl'][ck] = cv;

                del d['days'][x]
   
    return d

def compmonth(d):
    # sort accumulated countries              
    for x in d['days']:
        if len(x) == 6:
            d['days'][x]['countries'] = dict(sorted(d['days'][x]['countries'].items(), key=lambda item: item[1], reverse=True))

        # sort accumulated topurl
        for x in d['days']:
            if len(x) == 6:
                 if 'topurl' in d['days'][x]:
                     tmpTopUrl = dict(sorted(d['days'][x]['topurl'].items(), key=lambda item: item[1], reverse=True))
                     i = 0
                     for k,v in tmpTopUrl:
                         i += 1
                         if i >= 24:
                             break
                         d['days'][x]['topurl'][k] = v
                     del tmpTopUrl
    return d

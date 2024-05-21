from copy import deepcopy
from datetime import datetime, timedelta

def summonth(d):
    
    # accumulate previous months:
    # beginning with the 15th day of the month: the previous month can be summarized:
    # 2024.02.15 => 2023.12
    # 2024.02.16 => 2024.01
    
    sumUntilDay = datetime.now() - timedelta(days=46)
    sumTill = sumUntilDay.strftime("%Y%m")
    print("accumulate until month: "  + sumTill)   # 202312
    
    # iterate over days to accumulate months:
    dtmp = deepcopy(d)
    for x in dtmp['days']:
        # if date has a day:
            if len(x) > 6:
                currMonth = x[0:6]
                if currMonth <= sumTill:
                    print("CurrMonth: " + currMonth + "  day x: " + x)
                    if currMonth not in d['days']:
                            
                        d['days'][currMonth] = {}
                        d['days'][currMonth]['hits']    = 0;
                        d['days'][currMonth]['visits'] = 0;
                        d['days'][currMonth]['bytes_sent']   = 0;
                        d['days'][currMonth]['countries'] = {}
                        d['days'][currMonth]['source'] = {}
                        d['days'][currMonth]['serverResponseCode'] = {}
                        
                        d['days'][currMonth]['device_hits'] = {} 
                        d['days'][currMonth]['device_hits']['mobile']  = 0 
                        d['days'][currMonth]['device_hits']['tablet']  = 0 
                        d['days'][currMonth]['device_hits']['desktop'] = 0 
                        d['days'][currMonth]['device_hits']['bots']    = 0 
                        d['days'][currMonth]['device_hits']['others']  = 0 
                                               
                    d['days'][currMonth]['hits'] += dtmp['days'][x]['hits']
                    d['days'][currMonth]['visits'] += dtmp['days'][x]['visits']
                    d['days'][currMonth]['bytes_sent']   += int(dtmp['days'][x]['bytes_sent'])

                    if 'countries' in dtmp['days'][x]:
                        for ck,cv in dtmp['days'][x]['countries'].items():
                            print("country: " + ck + ": " + str(cv) )
                            print("countries" + str(d['days'][currMonth]['countries']))
                            if ck in d['days'][currMonth]['countries']:
                                d['days'][currMonth]['countries'][ck] += cv
                            else:
                                d['days'][currMonth]['countries'][ck] = cv;
                    
                    d['days'][currMonth]['device_hits']['mobile']  += d['days'][x]['device_hits']['mobile']
                    d['days'][currMonth]['device_hits']['tablet']  += d['days'][x]['device_hits']['tablet']
                    d['days'][currMonth]['device_hits']['bots']    += d['days'][x]['device_hits']['bots']
                    d['days'][currMonth]['device_hits']['desktop'] += d['days'][x]['device_hits']['desktop']
                    d['days'][currMonth]['device_hits']['others']  += d['days'][x]['device_hits']['others']

                    # external sources:
                    if 'source' in dtmp['days'][x]:
                        for ck,cv in dtmp['days'][x]['source'].items():
                            print("external Source: " + ck + ": " + str(cv) )

                            print("eS" + str(d['days'][currMonth]['source']))
                            if ck in d['days'][currMonth]['source']:
                                d['days'][currMonth]['source'][ck] += cv
                            else:
                                d['days'][currMonth]['source'][ck] = cv;

                    # Server Response Code:
                    for ck,cv in dtmp['days'][x]['serverResponseCode'].items():
                        print("Responsecode: " + ck + ": " + str(cv) )

                        print("eS" + str(d['days'][currMonth]['serverResponseCode']))
                        if ck in d['days'][currMonth]['serverResponseCode']:
                            d['days'][currMonth]['serverResponseCode'][ck] += cv
                        else:
                            d['days'][currMonth]['serverResponseCode'][ck] = cv;

                    del d['days'][x]
        
            # sort accumulated countries              
            for x in d['days']:
                if len(x) == 6:
                    d['days'][x]['countries'] = dict(sorted(d['days'][x]['countries'].items(), key=lambda item: item[1], reverse=True))
   
    return d

from copy import deepcopy
from operator import itemgetter

# accumulate navigation to the last processed day of the month
# and compress topUrl to 40 entries
def sumDayV0001(d, verbosity ):
    
    # nav: accumulate nav on the last day of month:
    dtmp = deepcopy(d)
    lastDay = None
    for k, v in sorted(dtmp['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # consider only days:
        if len(k) < 8:
            continue

        # change of month or first iteration:
        if (lastDay is None 
                or lastDay[0:6] != k[0:6]):
            lastDay = k
            if "99" in verbosity:
                print("sumNavDayV0001: lastDay of Month is: " + str(lastDay) + " " + str(k))

        # do not process lastDay!
        if str(lastDay) == str(k):
            continue

        # prepare nav (might be at midnight!!)
        if 'user' not in d['v0001']['days'][lastDay]:
            d['v0001']['days'][lastDay]['user'] = {}
        if 'nav' not in d['v0001']['days'][lastDay]['user']:
            d['v0001']['days'][lastDay]['user']['nav'] = []
        
        # iterate though previous days
        if 'nav' in dtmp['v0001']['days'][k]['user']:
            for e in dtmp['v0001']['days'][k]['user']['nav']:
                found = False
                for f in d['v0001']['days'][lastDay]['user']['nav']:            
                    if (e['s'] == f['s']
                        and e['t'] == f['t']):
                        f['c'] += e['c']
                        found = True
                        break
                if found == False:
                    d['v0001']['days'][lastDay]['user']['nav'].append(e)
            del d['v0001']['days'][k]['user']['nav']

        
        # take max 40 TopUrl per Day:
        for k, v in sorted(dtmp['v0001']['days'].items(), key=itemgetter(0), reverse=True):
            # consider only days:
            if len(k) < 8:
                continue
            if 'topUrl' in dtmp['v0001']['days'][k]['user']:
                c = 0
                for t, u in sorted(dtmp['v0001']['days'][k]['user']['topUrl'].items(), key=lambda x: x[1], reverse=True):
                    c = c + 1
                    if c > 40:
                         try:
                           del d['v0001']['days'][k]['user']['topUrl'][t]
                         except KeyError:
                           print("sumDayV0001 key error: " +  str(t) +  " day:" + str(k) + " count: " + str(u) )
                
    return d

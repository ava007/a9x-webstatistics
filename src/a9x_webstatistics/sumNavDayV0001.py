from copy import deepcopy
from operator import itemgetter

# accumulate navigation to the last processed day of the month
def sumNavDayV0001(d):
    
    # nav: accumulate nav on the last day of month:
    lastDay = None
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # consider only days:
        if len(k) < 8:
            continue

        # change of month or first iteration:
        if (lastDay is None 
                or lastDay[0:6] != k[0:6]):
            lastDay = k
            print("sumNavDay: lastDay is: " + str(lastDay))

        # prepare last day and do not process it!
        if lastDay == k:
            if 'user' not in d['v0001']['days'][lastDay]:
                d['v0001']['days'][lastDay]['user'] = {}
            if 'nav' not in d['v0001']['days'][lastDay]['user']:
                d['v0001']['days'][lastDay]['user']['nav'] = []
            continue

        # iterate though previous days
        if 'nav' in d['v0001']['days'][k]['user']:
            for e in d['v0001']['days'][k]['user']['nav']:
                found = False
                for f in d['v0001']['days'][lastDay]['user']['nav']:            
                    if (e['s'] == f['s']
                        and e['t'] == f['t']):
                        e['c'] += f['c']
                    found = True
                    break
                if found == False:
                    d['v0001']['days'][lastDay]['user']['nav'].append(e)
            del d['v0001']['days'][k]['user']['nav']
        #print("\n sumNavDay user " + str(lastDay) + "\n "  + str(d['v0001']['days'][lastDay]['user']) )
    print("\n SuMNavDay 202402024: " + "\n " + str(d['v0001']['days']['20250224']['user']) )
    return d

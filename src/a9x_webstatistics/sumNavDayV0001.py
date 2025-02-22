from copy import deepcopy
from operator import itemgetter

# accumulate navigation to the last processed day of the month
def sumNavDayV0001(d):
    tmpNav = {}
    prevMonth = None
    for x in d['v0001']['days']:
        if prevMonth is None:
            prevMonth = x[0:6]
        if prevMonth != x[0:6]:
            if len(tmpNav) > 1:
                d['v0001']['days'][x]['user']['navigation'] = tmpNav
                tmpNav = {}
        if len(x) == 8 and 'navigation' in d['v0001']['days'][x]['user']:
            for ck,cv in sorted(d['v0001']['days'][x]['user']['navigation'].items(), key=itemgetter(1),reverse=False):
                if ck not in tmpNav:
                    tmpNav[ck] = cv
                else:
                    tmpNav[ck] += cv
                del d['v0001']['days'][x]['user']['navigation'][ck]
            del d['v0001']['days'][x]['user']['navigation']

    if len(tmpNav) > 1:
        d['v0001']['days'][x]['user']['navigation'] = tmpNav


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
            continue    # skip youngest day

        # prep youngest day:
        if 'user' not in d['v0001']['days'][lastDay]:
            d['v0001']['days'][lastDay]['user'] = {}
        if 'nav' not in d['v0001']['days'][lastDay]['user']:
            d['v0001']['days'][lastDay]['user']['nav'] = []

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
    return d

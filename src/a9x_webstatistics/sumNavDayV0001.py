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
           
    return d

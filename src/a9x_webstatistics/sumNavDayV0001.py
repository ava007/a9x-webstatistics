from copy import deepcopy
from operator import itemgetter

# accumulate navigation to the last processed day of the month
def sumNavDayV0001(d):
    
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
        #    print("sumNavDay: lastDay is: " + str(lastDay) )

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
    #            print("e: " + str(k) + " " + str(e))
                for f in d['v0001']['days'][lastDay]['user']['nav']:            
                    if (e['s'] == f['s']
                        and e['t'] == f['t']):
                        f['c'] += e['c']
                        found = True
                        break
                if found == False:
    #                print("e: appended: " + str(k) + " " + str(e))
                    d['v0001']['days'][lastDay]['user']['nav'].append(e)
            del d['v0001']['days'][k]['user']['nav']
    #        print("sumNavDayV0001: deleted: " + str(k))
    #try:
    #    print("\nsumNavDayV0001.py 20250223->user->nav: " + "\n " + str(dtmp['v0001']['days']['20250223']['user']['nav']) )
    #except KeyError:
    #    pass
    #try:
    #    print("\nsumNavDayV0001.py 20250224->user->nav: " + "\n " + str(d['v0001']['days']['20250224']['user']['nav']) )
    #except KeyError:
    #    pass   # do nothing
    return d

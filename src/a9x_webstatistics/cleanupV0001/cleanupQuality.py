from copy import deepcopy
from datetime import datetime, timedelta
from operator import itemgetter
import json

def cleanupQualityV0001(d):
    
    # delete quality older than 92 days:

    clnupUntilDay = datetime.now() - timedelta(days=92)
    clnupTill = clnupUntilDay.strftime("%Y%m")
    print("cleanupQualityV0001: purge quality entries before "  + str(clnupTill))
    
    # iterate over days to accumulate months:
    dtmp = deepcopy(d)
    for x in dtmp['v0001']['days']:
        # if date has a day:
        if len(x) > 6:
            continue
        if x >= clnupTill:
            continue
        if 'quality' in dtmp['v0001']['days'][x]:
            print("cleanupQuality: purged quality entries for " + str(x))
            del d['v0001']['days'][x]['quality']
    return d

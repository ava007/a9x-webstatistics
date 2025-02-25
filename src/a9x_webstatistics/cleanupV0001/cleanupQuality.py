from copy import deepcopy
from datetime import datetime, timedelta
from operator import itemgetter
import json

def cleanupQualityV0001(d, statfile):
    
    # delete quality older than 92 days:

    clupUntilDay = datetime.now() - timedelta(days=92)
    clupTill = sumUntilDay.strftime("%Y%m")
    print("cleanupQualityV0001: accumulate including month: "  + clupTill)
    
    # iterate over days to accumulate months:
    dtmp = deepcopy(d)
    for x in dtmp['v0001']['days']:
        # if date has a day:
        if len(x) > 6:
            continue
        if x >= clupTill:
            continue
        if 'quality' in dtmp['v0001']['days'][x]:
            print("cleanupQuality: delete quality in: " + str(x))

            

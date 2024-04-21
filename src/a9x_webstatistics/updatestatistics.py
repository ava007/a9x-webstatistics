def upd(
    d,
    i):
        
    dt = i['dt'].strftime("%Y%m%d")

    # init a new day with minimal attributes:
    if dt not in d['days']:
        d['days'][dt] = {}
        d['days'][dt]['hits']    = 0;
        d['days'][dt]['visits']  = 1;
        d['days'][dt]['size']    = 0;
        d['days'][dt]['serverResponseCode'] = {}

    # update statistics
    d['days'][dt]['hits'] = d['days'][dt]['hits'] + 1
    d['timelastrec'] = i['dt'].strftime("%Y%m%d%H%M%S")
        
    return d

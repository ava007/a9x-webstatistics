def upd(
    d,
    i,
    visitIP):
        
    dt = i['ymd']

    # init a new day with minimal attributes:
    if dt not in d['days']:
        d['days'][dt] = {}
        d['days'][dt]['hits']    = 0;
        d['days'][dt]['visits']  = 0;
        d['days'][dt]['bytes_sent'] = 0;
        d['days'][dt]['serverResponseCode'] = {}

    # update statistics
    d['days'][dt]['hits'] = d['days'][dt]['hits'] + 1
    d['days'][dt]['bytes_sent'] = str(int(d['days'][dt]['bytes_sent']) + int(i['bytes_sent']))

    if i['status'] in d['days'][dt]['serverResponseCode']:
        d['days'][dt]['serverResponseCode'][i['status']] += 1
    else:
        d['days'][dt]['serverResponseCode'][i['status']] = 1
        
    d['timelastrec'] = i['timestamp']

    if i['ip'] not in visitIP:
        d['days'][dt]['visits'] = d['days'][dt]['visits'] + 1;
        visitIP[i['ip']] = 1
        
    return d

def migv0001(
    d,
    ):
    # return if already migrated:
    if 'v0001' in d:
        return
    d['v0001'] = {}
    d['v0001']['days'] = {}
    for x in d['days']:
        d['v0001']['days'][x] = {}
        d['v0001']['days'][x]['user'] = {}
        d['v0001']['days'][x]['robots'] = {}
        d['v0001']['days'][x]['quality'] = {}

    # write updated statistic file:
    with open('webstatv0001.json', "w") as sf:
       json.dump(d,sf)  

        


# -*- coding: utf-8 -*-
import ipaddress
from operator import itemgetter

# performance for the last 31 days:
def performance(d):
    time_count = 0
    time_sum = 0
    cache_miss = 0
    cache_hit = 0
    cache_unknown = 0
    ic = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # dont take months in account:
        if len(k) <= 6:
            continue
        if 'performance' in d['v0001']['days'][k]:
            if 'response_time' in d['v0001']['days'][k]['performance']:
                if 'time_count' in d['v0001']['days'][k]['performance']['response_time']:
                    time_count += d['v0001']['days'][k]['performance']['response_time']['time_count']
                    time_sum += d['v0001']['days'][k]['performance']['response_time']['time_sum']
            if 'cache' in d['v0001']['days'][k]['performance']:
                ic += 1
                if 'MISS' in d['v0001']['days'][k]['performance']['cache']:
                    cache_miss += d['v0001']['days'][k]['performance']['cache']['MISS']
                if 'HIT' in d['v0001']['days'][k]['performance']['cache']:
                    cache_hit += d['v0001']['days'][k]['performance']['cache']['HIT']
                if 'unknown' in d['v0001']['days'][k]['performance']['cache']:
                    cache_unknown += d['v0001']['days'][k]['performance']['cache']['unknown']
        if ic >= 31:
            break
      
    h = ''
    if time_count > 0 or cache_miss > 0:                
        h += '<div class="col-md-12 col-lg-6 col-xxl-6">'
        h += '<h3 class="card-title">Performance for the last ' + str(ic) + ' days</h3>'
        h += '<table class="table">'
        if time_count > 0:
            h += '<tr>'
            h += '<td>Average Response Time for internal processing:</td><td>{:.2} Seconds</td>'.format(time_sum/time_count)
            h += '</tr>'
        if cache_hit > 0:
            h += '<tr>'
            h += '<td>Cache Hit Ratio:</td><td>{:.0%}</td>'.format(cache_hit / (cache_hit+cache_miss+cache_unknown) )
            h += '</tr>'
        h += '</table>'
        h += '</div>'
    return h

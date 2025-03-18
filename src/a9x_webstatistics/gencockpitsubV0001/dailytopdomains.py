# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

def dailyTopDomains(d, owndomain, omit):
  day_usr_i = 0
  tsource = {}
  for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
    # consider only days:
    if len(k) < 8:
      continue
    # show at max 31 days:
    if day_usr_i >= 31:
      break
    day_usr_i += 1

    # top 10 source domains:
    if 'nav' in d['v0001']['days'][k]['user']:
      # sort by count e['c'] desc:
      for e in sorted(d['v0001']['days'][k]['user']['nav'], key=lambda x: x['c'], reverse=True):
        if 'p' not in e:   # internal links
          continue
        if e['s'] in omit:
          continue
        if e['t'] in omit:
          continue
        if e['s'] not in tsource:
          tsource[e['s']] = 0
        tsource[e['s']] += e['c']
  if len(tsource) == 0:
    return ''
  # Top 10 Domains on daily basis
  h += '<div class="row pt-3"><div class="col-md-12 col-lg-6 col-xxl-6">'
  h += '<h3 class="card-title">Top 10 Domains for the last ' + str(day_usr_i) + ' days</h3>'
  h += '<p class="card-text">User hits refering to external domain:</p>'
  h += '<table class="table">'
  h += '<thead><tr><th scope="col" style="text-align: left">Rank</th><th scope="col" style="text-align: left">Domain</th><th scope="col" style="text-align: right">Hit Count</th></tr></thead>'
  i = 1
  for k, v in sorted(tsource.items(), key=itemgetter(1), reverse=True):
    if owndomain in k:
      continue
    # prevent IP or domains with special characters:
    if any( x in k for x in {'[', ']', ':'} ):
      continue
    if is_valid_ip(k) == True:  # to suppress ip; ip is not a domain anyway    
      continue
    h += '<tr><td>' + str(i) + '.</td><td>' + str(k) + '</td><td style="text-align: right">' + str(format(v, ',')) + '</td></tr>'
      i += 1
    if i > 10:
      break
    h += '</table>'
    h += '</div>'  + "\n"   # end of col and card
 
    return h

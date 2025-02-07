# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

def addlink(links, linkentry):
    duplicate_found = False
    for li in links:
        if (li['source'] == linkentry['source']
            and li['target'] == linkentry['target']):
                duplicate_found = True
                li['value'] += linkentry['value']
                break
                if entrylink['target'] == li['source']:  # prevent circular links
                    duplicate_found = True
                    break
    if duplicate_found == False:
        links.append(entrylink)
    return links
    
# navigation chart as sankey diagram:
def makenodeslinks(d, owndomain, omit):
    links = []    # {'source': 'googlecom', 'target': 'teamviewax', 'c': 1}
    nodes = []    # {'id': 'googlecom', 'value':1, 'name': 'google.com'}

    # externalFriendsHits:
    days = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit months or years:
        if len(k) <= 6:
            continue
        days += 1
        if 'externalFriendsHits' in d['v0001']['days'][k]['user']:
            for tk, tv in d['v0001']['days'][k]['user']['externalFriendsHits'].items():
                if is_valid_ip(tk) == True:  # to suppress ip; ip is not a domain anyway    
                    continue
                if '[' in tk:    # hack for IPv6 addresses
                    continue
                tmplink = {}
                tmplink['source'] =  "".join(map(lambda char: char if char.isalnum()  else "", tk) ) # eliminate special chars
                tmplink['value'] = 1
                for tdk,tdv in tv['target'].items():
                    if any(oelm in tdk for oelm in omit):  # don not show parts of url 
                        continue
                    tmplink['target'] =  "".join(map(lambda char: char if char.isalnum()  else "", tdk) ) # eliminate special chars
                    if tmplink['target'] == '/':    # to avoid empty nb
                        tmplink['target'] = owndomain
                    duplicate_found = False
                    for li in links:
                        if (li['source'] == tmplink['source']
                                and li['target'] == tmplink['target']):
                            duplicate_found = True
                            li['value'] += tdv
                            break
                        if tmplink['target'] == li['source']:  # prevent circular links
                            duplicate_found = True
                            break

                    if duplicate_found == False:
                        links.append(tmplink)

                    n[0] = tmplink['source'] # tk
                    n[1] = tmplink['target'] #tdk
                    for i in range(2):   # n[0] and n[1]
                        tmpnode = {}
                        tmpnode['name'] = n[i]
                        tmpnode['typ'] = 'root'
                        duplicate_found = False
                        tmpnode['id'] = "".join(map(lambda char: char if char.isalnum()  else "", n[i]) ) # eliminate special chars
                        for no in nodes:
                            if (no['id'] == tmpnode['id']):
                                duplicate_found = True
                                break
                    
                        if duplicate_found == False:
                            nodes.append(tmpnode)
                days += 1
                if days > 31:
                    break


    
    days = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        if len(k) < 8:   # not a day anymore
            break
        if 'user' in d['v0001']['days'][k] and 'navigation' in d['v0001']['days'][k]['user']:
            for sk,sv in d['v0001']['days'][k]['user']['navigation'].items():
                n = sk.split('(())') 
                if n[0] == n[1]:
                    continue
                if len(n[0]) == 0 or len(n[1]) == 0:
                    continue
                # allow only a-z and 0-9:
                if n[0] == '/':    # to avoid empty na
                    n[0] = owndomain
                if n[1] == '/':    # to avoid empty nb
                    n[1] = owndomain
                if any(oelm in n[0] for oelm in omit):  # do not show parts of url 
                    continue
                if any(oelm in n[1] for oelm in omit):  # do not show parts of url 
                    continue
                tmplink = {}
                tmplink['source'] = "".join(map(lambda char: char if char.isalnum()  else "", n[0]) ) # eliminate special chars
                tmplink['target'] = "".join(map(lambda char: char if char.isalnum()  else "", n[1]) ) # eliminate special chars
                tmplink['value'] = sv
                duplicate_found = False
                for li in links:
                    if (li['source'] == tmplink['source']
                            and li['target'] == tmplink['target']):
                        duplicate_found = True
                        li['value'] += sv
                        break
                    if tmplink['target'] == li['source']:  # prevent circular links
                        duplicate_found = True
                        break
                if duplicate_found == False:
                    links.append(tmplink)

                # add nodes if not already in array:
                n[0] = tmplink['source']
                n[1] = tmplink['target']
                for i in range(2):   # n[0] and n[1]
                    tmpnode = {}
                    tmpnode['name'] = n[i]
                    if n[i][0:1] != '/':
                        tmpnode['typ'] = 'root'
                    duplicate_found = False
                    tmpnode['id'] = "".join(map(lambda char: char if char.isalnum()  else "", n[i]) ) # eliminate special chars
                    for no in nodes:
                        if (no['id'] == tmpnode['id']):
                            duplicate_found = True
                            break
                    
                    if duplicate_found == False:
                        nodes.append(tmpnode)
            
        days += 1
        if days > 31:
            break

    return nodes, links

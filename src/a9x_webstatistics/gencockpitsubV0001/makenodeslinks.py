# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

def addlink(links, linkentry, owndomain):

    if linkentry['target'] == linkentry['source']:  # prevent circular links
        return links

    if linkentry['source'] == '/' or len(linkentry['source']) == 0:
        linkentry['source'] = owndomain

    if linkentry['target'] == '/' or len(linkentry['source']) == 0:
        linkentry['target'] = owndomain

    # check if links already exists:
    duplicate_found = False
    for li in links:
        if (li['source'] == linkentry['source']
            and li['target'] == linkentry['target']):
                duplicate_found = True
                li['value'] += linkentry['value']
                break
    
    # check for circular links:  ie. new target must not be in existing source
    for li in links:
        if li['source'] == linkentry['target']:
            duplicate_found = True
            break
    
    if duplicate_found == False:
        links.append(linkentry)
    #print("linkadd: " + str(duplicate_found) + " " + str(linkentry) )
    return links

def addnode(nodes, node, owndomain):

    if node['name'] == '/' or len(node['name']) == 0:
        node['name'] = owndomain

    if node['id'] == '/'  or len(node['id']) == 0:
        node['id'] = "".join(map(lambda char: char if char.isalnum()  else "", owndomain) ) # eliminate special chars

    # assert for sorting:
    if 'co' not in node:  
        node['co'] = 0     # count outgoing
        
    # check if node already exists:
    duplicate_found = False
    for no in nodes:
        if no['id'] == node['id']:
            duplicate_found = True
            break
    if duplicate_found == False:
        nodes.append(node)
    return nodes

# make nodes and links based on nav 20250221:
def makeNodesLinks2(dz, owndomain, omit, daysback=31):
    # temporary and for testing only:
    #dz['v0001'] = {}
    #dz['v0001']['days'] = {}
    #dz['v0001']['days']['20250228'] = {}
    #dz['v0001']['days']['20250228']['user'] = {}
    #dz['v0001']['days']['20250228']['user']['nav'] = [{"s": "pypi.org", "t": "/webstatsLF24.html", "p": "e", "c": 1}, {"s": "/", "t": "/kl/add/", "c": 1}, {"s": "/", "t": "/team/login/", "c": 1}, {"s": "/", "t": "/team/view/comparison%20team/", "c": 1}, {"s": "/", "t": "/kl/view/526f7142-abb1-4374-8020-e0c05266a988/", "c": 1}, {"s": "/xadm/log/a", "t": "/xadm/log/c", "c": 1}, {"s": "www.google.com", "t": "/", "c": 1}, {"s": "/", "t": "/kl/view/ef936637-2e83-482c-ac23-a3a7ffa10e17/", "c": 1}, {"s": "/", "t": "/kl/view/3deec972-5839-4a71-bd70-e2c886b83fda/", "c": 1}, {"s": "/", "t": "/kl/view/39575f54-e28f-4d97-bd6d-c7330cfd9d3c/", "c": 1}, {"s": "/", "t": "/kl/search/", "c": 1}, {"s": "/kl/search/", "t": "/", "c": 1}, {"s": "/team/viewtangledtree/ax/", "t": "/team/tag/ax/health/", "c": 1}, {"s": "/team/tag/ax/health/", "t": "/kl/view/bb0cd53a-cbf2-4fa2-9ae2-3a20fa7cc43f/", "c": 1}, {"s": "/kl/view/bb0cd53a-cbf2-4fa2-9ae2-3a20fa7cc43f/", "t": "/team/tag/ax/top10/", "c": 1}, {"s": "/team/tag/ax/top10/", "t": "/kl/view/f95c0c51-5f00-42f6-ae4c-50abb30ed665/", "c": 1}, {"s": "/", "t": "/kl/view/6c503f98-135e-4ade-81f0-9db92cc1fb05/", "c": 1}, {"s": "/xadm/sts", "t": "/xadm/log/a", "c": 2}, {"s": "/", "t": "/team/view/ax/", "c": 2}, {"s": "/", "t": "/kl/view/a05898ce-e766-4450-b0de-35a35c321097/", "c": 3}, {"s": "/team/view/ax/", "t": "/team/viewtangledtree/ax/", "c": 3}, {"s": "", "t": "/", "c": 56}, {"s": "google.com", "t": "/kl/view/a05898ce-e766-4450-b0de-35a35c321097/", "p": "e", "c": 5}, {"s": "google.de", "t": "/kl/view/6c503f98-135e-4ade-81f0-9db92cc1fb05/", "p": "e", "c": 1}, {"s": "cityfitness-eisenberg.de", "t": "/", "p": "e", "c": 1}, {"s": "google.com", "t": "/kl/view/3deec972-5839-4a71-bd70-e2c886b83fda/", "p": "e", "c": 5}, {"s": "google.com", "t": "/kl/view/39575f54-e28f-4d97-bd6d-c7330cfd9d3c/", "p": "e", "c": 1}, {"s": "google.com", "t": "/kl/view/abc909f2-10f6-4390-a153-ce597291a8db/", "p": "e", "c": 4}, {"s": "quora.com", "t": "/", "p": "e", "c": 1}, {"s": "yandex.ru", "t": "/kl/view/ef936637-2e83-482c-ac23-a3a7ffa10e17/", "p": "e", "c": 2}, {"s": "github.com", "t": "/webstatsLF24.html", "p": "e", "c": 1}, {"s": "google.de", "t": "/kl/view/abc909f2-10f6-4390-a153-ce597291a8db/", "p": "e", "c": 1}, {"s": "google.com", "t": "/", "p": "e", "c": 2}]
        
    links = []    # {'source': 'googlecom', 'target': 'teamviewax', 'c': 1}
    nodes = []    # {'id': 'googlecom', 'value':1, 'name': 'google.com'}

    days = 0
    for k, v in sorted(dz['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit months or years:
        if len(k) <= 6:
            continue
        days += 1
        if 'nav' in dz['v0001']['days'][k]['user']:
            for e in dz['v0001']['days'][k]['user']['nav']:
                if is_valid_ip(e['s']) == True:  # to suppress ip; ip is not a domain anyway    
                    continue
                if '[' in e['s']:    # hack for IPv6 addresses
                    continue
                if ':' in e['s']:    # hack for IPv6 addresses/ports
                    continue

                tmpnode1 = {}
                tmpnode1['name'] = e['s']
                if tmpnode1['name'] == '/': 
                    tmpnode1['name'] = owndomain
                tmpnode1['id'] = "".join(map(lambda char: char if char.isalnum()  else "", tmpnode1['name']) ) # eliminate special chars
                tmpnode1['co'] = e['c']   # count outgoing
                nodes = addnode(nodes, tmpnode1, owndomain)

                tmpnode2 = {}
                tmpnode2['name'] = e['t']
                if tmpnode2['name'] == '/': 
                    tmpnode2['name'] = owndomain
                tmpnode2['id'] = "".join(map(lambda char: char if char.isalnum()  else "", tmpnode2['name']) ) # eliminate special chars
                tmpnode1['ci'] = e['c']  # count incoming
                nodes = addnode(nodes, tmpnode1, owndomain)
                
                tmplink = {}
                tmplink['source'] = tmpnode1['id']
                tmplink['target'] = tmpnode2['id']
                tmplink['value'] = e['c']
                links = addlink(links, tmplink, owndomain)
                    
        days += 1
        if days > daysback:
            break

    return nodes, links
    
# navigation chart as sankey diagram:
def makeNodesLinks(d, owndomain, omit, daysback=31):
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
                if ':' in tk:    # hack for IPv6 addresses/ports
                    continue

                tmpnode = {}
                tmpnode['name'] = tk
                if tmpnode['name'] == '/': 
                    tmpnode['name'] = owndomain
                tmpnode['id'] = "".join(map(lambda char: char if char.isalnum()  else "", tmpnode['name']) ) # eliminate special chars
                tmpnode['typ'] = 'root'
                nodes = addnode(nodes, tmpnode, owndomain)
                tmplink = {}
                tmplink['source'] =  "".join(map(lambda char: char if char.isalnum()  else "", tmpnode['name']) ) # eliminate special chars
                for tdk,tdv in tv['target'].items():
                    if any(oelm in tdk for oelm in omit):  # don not show parts of url 
                        continue
                    if tdk == '/':
                        tdk2 = owndomain
                    else:
                        tdk2 = tdk
                    tmplink['target'] =  "".join(map(lambda char: char if char.isalnum()  else "", tdk2) ) # eliminate special chars
                    tmplink['value'] = tdv
                    links = addlink(links, tmplink, owndomain)
                    
                    tmpnode = {}
                    tmpnode['name'] = tdk2
                    tmpnode['id'] = "".join(map(lambda char: char if char.isalnum()  else "", tdk2) ) # eliminate special chars
                    nodes = addnode(nodes, tmpnode, owndomain)
                days += 1
                if days > daysback:
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
                    links = addlink(links, tmplink, owndomain)

                    node = {}
                    node['id'] = "".join(map(lambda char: char if char.isalnum()  else "", n[0]) ) # eliminate special chars
                    node['name'] = n[0]
                    addnode(nodes, node, owndomain)

                    node = {}
                    node['id'] = "".join(map(lambda char: char if char.isalnum()  else "", n[1]) ) # eliminate special chars
                    node['name'] = n[1]
                    addnode(nodes, node, owndomain)
                
            days += 1
            if days > daysback:
                break

    return nodes, links

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

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
    if duplicate_found == False:
        links.append(linkentry)
    #print("linkadd: " + str(duplicate_found) + " " + str(linkentry) )
    return links

def addnode(nodes, node, owndomain):

    if node['name'] == '/' or len(node['name']) == 0:
        node['name'] = owndomain

    if node['id'] == '/'  or len(node['id']) == 0:
        node['id'] = "".join(map(lambda char: char if char.isalnum()  else "", owndomain) ) # eliminate special chars
        
    # check if node already exists:
    duplicate_found = False
    for no in nodes:
        if no['id'] == node['id']:
            duplicate_found = True
            break
    if duplicate_found == False:
        nodes.append(node)
    return nodes
    
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

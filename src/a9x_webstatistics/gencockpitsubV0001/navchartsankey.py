# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart as sankey diagram:
def navchartsankey(d, owndomain, omit):
    h = ''
    links = []    # {'source': 'google.com', 'target': '/team/view/ax', 'c': 1}
    nodes = []    # {'id': 'google.com', 'value':1}
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
                for i in range(2):   # n[0] and n[1]
                    tmpnode = {}
                    tmpnode['name'] = n[i]
                    #if ('.com' in n[i] or
                    #       '.ru' in n[i]):
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
                tmplink['value'] = 0
                for tdk,tdv in tv['target'].items():
                    if any(oelm in tdk for oelm in omit):  # don not show parts of url 
                        continue
                    tmplink['target'] =  "".join(map(lambda char: char if char.isalnum()  else "", tdk) ) # eliminate special chars
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

                    n[0] = tk
                    n[1] = tdk
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

                    
 
    # d3js horizontal bubble char in case results are available:
    h += '<script src="https://cdn.jsdelivr.net/npm/d3-sankey@0.12.3/dist/d3-sankey.min.js"></script>'
    h += "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
    h += '<div class="card mt-2"><div class="card-body">'
    h += '<h3 class="card-title">Navigation Chart</h3>'
    h += '<p class="card-text">User Navigation Chart for ' + owndomain + ':</p>'
    h += '<div id="navchart-container20250128"><svg id="svgchart20250128" width="600" height="400"></svg></div>'
    h += '<script type="module">' + "\n"
    h += 'const nodes = ' + str(nodes) + ';' + "\n"
    h += 'const links = ' + str(links) + ';' + "\n"
    h += 'const rect = document.getElementById("navchart-container20250128").getBoundingClientRect();'
    h += 'const margin = { top: 1, right: 20, bottom: 5, left: 1 };'
    h += 'const width = Math.round(rect.width) - margin.left - margin.right;'
    h += 'const height = width;'  + "\n"   # make height at least as width

    #  Convert the source and target to internal node indices
    h += 'const LS = d3.map(links, (link) => link.source);'
    h += 'const LT = d3.map(links, (link) => link.target);'
    h += 'const LV = d3.map(links, (link) => link.value);'

    h += 'const N = d3.map(nodes, (node) => node.id);'
    h += 'const G = null;'   # No specific node groups in this case

    #// Create a sankey layout
    h += 'const sankey = d3.sankey()'
    h += '.nodeId(({ index: i }) => N[i])'
    h += '.nodeWidth(10)'
    h += '.nodePadding(10)'
    h += '.nodeAlign(d3.sankeyJustify)'
    h += '.extent(['
    h += '[margin.left, margin.top],'
    h += '[width - margin.right, height - margin.bottom]'
    h += ']);'  + "\n"

    h += 'const { nodes: computedNodes, links: computedLinks } = sankey({'
    h += 'nodes: nodes,'
    h += 'links: links'
    h += '});'  + "\n"

    #// Create the SVG container
    h += 'const svg = d3.select("#svgchart20250128")'
    h += '.attr("width", width)'
    h += '.attr("height", height)'
    h += '.attr("viewBox", [0,0 , width, height])'
    h += '.attr("style", "max-width: 100%; height: auto;  font: 10px sans-serif; height: intrinsic;");'  + "\n"

    # // Add node elements (rectangles)
    h += 'const node = svg'
    h += '.append("g")'
    h += '.attr("stroke", "currentColor")'
    h += '.selectAll("rect")'
    h += '.data(computedNodes)'
    h += '.join("rect")'
    h += '.attr("x", (d) => d.x0)'
    h += '.attr("y", (d) => d.y0)'
    h += '.attr("width", (d) => d.x1 - d.x0)'
    h += '.attr("height", (d) => d.y1 - d.y0)'
    h += '.attr("fill", "#1f77b4");'  + "\n"

    #// Add labels to the nodes
    h += 'svg'
    h += '.append("g")'
    h += '.attr("font-family", "sans-serif")'
    h += '.attr("font-size", 10)'
    h += '.selectAll("text")'
    h += '.data(computedNodes)'
    h += '.join("text")'
    h += '.attr("x", (d) => (d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6))'
    h += '.attr("y", (d) => (d.y1 + d.y0) / 2)'
    h += '.attr("dy", "0.35em")'
    h += '.attr("text-anchor", (d) => (d.x0 < width / 2 ? "start" : "end"))'
    h += '.text((d) => d.id);'  + "\n"

    #// Add link elements (paths)
    h += 'const link = svg'
    h += '.append("g")'
    h += '.attr("fill", "none")'
    h += '.attr("stroke-opacity", 0.5)'
    h += '.selectAll("g")'
    h += '.data(computedLinks)'
    h += '.join("g");'  + "\n"

    h += 'link'
    h += '.append("path")'
    h += '.attr("d", d3.sankeyLinkHorizontal())'
    h += '.attr("stroke", "#ccc")'
    h += '.attr("stroke-width", (d) => Math.max(1, d.width));'  + "\n"

    #// Add titles to the links
    h += 'link'
    h += '.append("title")'
    h += '.text((d) => `${d.source.id} → ${d.target.id}\n${d.value}`);'  + "\n"

    h += '</script>'
    h += '</div></div></div>'
    return h

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

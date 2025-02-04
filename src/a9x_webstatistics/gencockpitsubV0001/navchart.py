# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart:
def navchart(d, owndomain, omit):
    h = ''
    links = []    # [{'source': 'google.com', 'target': '/team/view/ax', 'cnt': 2, 'source': 'bing.com', 'target': '/team/viex/comp', 'cnt': 5}]
    nodes = []    # [{'id': 'google.com', 'root': 'y', 'cnt_in': 1, 'cnt_out': 2}, {'id': '/team/view/ax/', 'cnt_in': 2, 'cnt_out': 1}]
    days = 0

    # create tmp array from all links from navigation
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
                tmplink['cnt'] = sv
                duplicate_found = False
                for li in links:
                    if (li['source'] == tmplink['source']
                            and li['target'] == tmplink['target']):
                        duplicate_found = True
                        li['cnt'] += sv
                        break
                if duplicate_found == False:
                    links.append(tmplink)

                for i in range(2):   # n[0] and n[1]
                    tmpnode = {}
                    tmpnode['name'] = n[i]
                    tmpnode['cnt_in'] = 0
                    tmpnode['cnt_out'] = 0
                    #if ('.com' in n[i] or
                    #       '.ru' in n[i]):
                    #    tmpnode['root'] = 'y'
                    duplicate_found = False
                    tmpnode['id'] = "".join(map(lambda char: char if char.isalnum()  else "", n[i]) ) # eliminate special chars
                    if i == 0:
                        tmpnode['cnt_in'] = tmplink['cnt']
                    else:
                        tmpnode['cnt_out'] = tmplink['cnt']
                    
                    for no in nodes:
                        if (no['id'] == tmpnode['id']):
                            duplicate_found = True
                            if i == 0:
                                no['cnt_in'] += tmpnode['cnt_in']
                            else:
                                no['cnt_out'] += tmpnode['cnt_out']
                            break
                    
                    if duplicate_found == False:
                        nodes.append(tmpnode)
            
        days += 1
        if days > 31:
            break

    days = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit months or years:
        if len(k) < 8:
            break
        days += 1
        if 'externalFriendsHits' in d['v0001']['days'][k]['user']:
            for tk, tv in d['v0001']['days'][k]['user']['externalFriendsHits'].items():
                if is_valid_ip(tk) == True:  # to suppress ip; ip is not a domain anyway    
                    continue
                if '[' in tk:    # hack for IPv6 addresses
                    continue
                tmplink = {}
                tmplink['source'] =  "".join(map(lambda char: char if char.isalnum()  else "", tk) ) # eliminate special chars
                tmplink['cnt'] = 0
                for tdk,tdv in tv['target'].items():
                    if any(oelm in tdk for oelm in omit):  # don not show parts of url 
                        continue
                    if tdk == '/':
                        tmplink['target'] = "".join(map(lambda char: char if char.isalnum()  else "", owndomain) ) # eliminate special chars
                    else:
                        tmplink['target'] =  "".join(map(lambda char: char if char.isalnum()  else "", tdk) ) # eliminate special chars
                    duplicate_found = False
                    for li in links:
                        if (li['source'] == tmplink['source']
                                and li['target'] == tmplink['target']):
                            duplicate_found = True
                            li['cnt'] += tdv
                            break
                    if duplicate_found == False:
                        links.append(tmplink)

                    n[0] = tk
                    n[1] = tdk
                    for i in range(2):   # n[0] and n[1]
                        tmpnode = {}
                        tmpnode['name'] = n[i]
                        tmpnode['cnt_in'] = 0
                        tmpnode['cnt_out'] = 0
                        tmpnode['root'] = 'y'
                        duplicate_found = False
                        tmpnode['id'] = "".join(map(lambda char: char if char.isalnum()  else "", n[i]) ) # eliminate special chars
                        for no in nodes:
                            if (no['id'] == tmpnode['id']):
                                duplicate_found = True
                                if i == 0:
                                    no['cnt_in'] += tmpnode['cnt_in']
                                else:
                                    no['cnt_out'] += tmpnode['cnt_out']
                                break
                    
                        if duplicate_found == False:
                            nodes.append(tmpnode)
                days += 1
                if days > 31:
                    break


    # start with the top 10 root nodes sorted by  'cnt_out' 
    root_nodes = [item for item in nodes if item.get('root') == 'y']
    top_nodes = sorted(root_nodes, key=lambda x: x['cnt_out'], reverse=True)
    print("top_nodes: " + str(top_nodes) )

    chart_links = []
    chart_nodes = []
    for n in top_nodes:
        for li in links:
            if n['id'] == li['source']:
                chart_links.append(li)
                # check source_node:
                cn_found = False
                for cn in chart_nodes:
                    if li['source'] == cn['id']:
                        cn_found = True
                if cn_found == False:
                    tmpnode = {}
                    tmpnode['id'] = li['source']
                    tmpnode['name'] = li['source']
                    for nn in nodes:
                        if nn['id'] == li['source']:
                            tmpnode['name'] = nn['name']
                            break
                    if n['root'] == 'y':
                        tmpnode['root'] = 'y'
                    chart_nodes.append(tmpnode)
                # check target_node:
                cn_found = False
                for cn in chart_nodes:
                    if li['target'] == cn['id']:
                        cn_found = True
                if cn_found == False:
                    tmpnode = {}
                    tmpnode['name'] = li['target']
                    tmpnode['id'] = li['target']
                    for nn in nodes:
                        if nn['id'] == li['target']:
                            tmpnode['name'] = nn['name']
                            break
                    chart_nodes.append(tmpnode)

    # find 2nd level links/nodes
    for n2 in chart_nodes:
        if 'root' in n2:
            continue
        for l2 in links:
            if n2['id'] == li['source']:
                tmplink = {}
                tmplink['source'] =  li['source']
                tmplink['target'] =  li['target']
                tmplink['cnt'] = 1
                chart_links.append(tmplink)
                cn_found = False
                for cn in chart_nodes:
                    if li['target'] == cn['id']:
                        cn_found = True
                        break
                if cn_found == False:
                    tmpnode = {}
                    tmpnode['id'] = li['target']
                    tmpnode['name'] = li['target']
                    chart_nodes.append(tmpnode)
                break
 
    # d3js horizontal bubble char in case results are available:
    h += "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
    h += '<div class="card mt-2"><div class="card-body">'
    h += '<h3 class="card-title">Navigation Chart</h3>'
    h += '<p class="card-text">User Navigation Chart for ' + owndomain + ':</p>'
    h += '<div id="navchart-container"><svg id="svgchart" width="600" height="400"></svg></div>'
    h += '<script type="module">' + "\n"
    h += 'const nodes = ' + str(chart_nodes) + ';' + "\n"
    h += 'const links = ' + str(chart_links) + ';' + "\n"
    h += 'const rect = document.getElementById("navchart-container").getBoundingClientRect();'
    h += 'const margin = { top: 20, right: 20, bottom: 40, left: 100 };'
    h += 'const width = Math.round(rect.width) - margin.left - margin.right;'
    #h += 'const height = 400 - margin.top - margin.bottom;'  + "\n"
    h += 'const height = width;'  + "\n"   # make height at least as width

    # 2. Set up the SVG container and set dimensions
    h += 'const svg = d3.select("#svgchart").attr("width", width).attr("height", height);'
      
    # 3. Set up the D3 force simulation
    h += "const validLinks = links.filter(link => link.source && link.target);"
    h += "const simulation = d3.forceSimulation(nodes)"
    h += ".force('link', d3.forceLink(validLinks).id(d => d.id).distance(100))"
    h += ".force('charge', d3.forceManyBody().strength(-300))"
    h += ".force('center', d3.forceCenter(width / 3, height / 2));"  + "\n"

    # 4. Create links (edges)
    h += "const link = svg.append('g')"
    h += ".selectAll('.link')"
    h += ".data(links)"
    h += ".enter().append('line')"
    h += ".style('stroke','#999')"
    h += ".style('stroke-opacity','0.6');" + "\n"
    #h += ".attr('class', 'link');"  + "\n"

    # 5. Create nodes
    h += "const node = svg.append('g')"
    h += ".selectAll('.node')"
    h += ".data(nodes)"
    h += ".enter().append('circle')"
    h += ".attr('class', 'node')"
    h += ".attr('r', 10)"
    h += ".style('fill','lightskyblue')"
    h += ".style('stroke','white')"
    h += ".style('stroke-width','1.5px')"
    h += ".call(d3.drag()"
    h += ".on('start', dragStarted)"
    h += ".on('drag', dragged)"
    h += ".on('end', dragEnded));" + "\n"

    # 6. Add labels to the nodes
    h += "const labels = svg.append('g').selectAll('.label')"
    h += ".data(nodes)"
    h += ".enter()"
    h += ".append('a')"
    h += ".attr('xlink:href', d => d.name.startsWith('/') ? `https://" + owndomain + "${d.name}` : 'https://' + d.name)"
    h += ".attr('target', '_blank')"  # Open in new tab
    h += ".append('text')"
    h += ".style('font-family','Arial, sans-serif')"
    h += ".style('font-size','10px')"
    h += ".style('fill', 'blue')"  # Make it look like a link
    h += ".style('text-decoration', 'underline')"
    h += ".attr('dx', 25)"
    h += ".attr('dy', '.35em')"
    h += ".text(d => {"
    h += "  let lbl;"
    h += "  if (d.name.length > 15) {"
    h += "    lbl = d.name.substring(0,10) + '...' + d.name.slice(-3);"
    h += "  } else {"
    h += "    lbl = d.name;"
    h += "  }"
    h += "  return lbl; }"
    h += ");"  + "\n"

    # 7. Place root nodes along the left side of the screen and freeze their positions
    h += "const rootNodes = nodes.filter(n => n.root === 'y');"
    h += "rootNodes.forEach((node, index) => {"
    h += "node.x = 100;" # Set all root nodes on the left (x = 100)
    h += "node.y = 100 + index * 100;"   # Distribute vertically along a line
    h += "node.fx = node.x;"  # Freeze position
    h += "node.fy = node.y;"  # Freeze position
    h += "d3.selectAll('circle.node').filter(d => d && d.id === node.id).style('fill', 'red');"  # color red
    h += "});"  + "\n"

    # 8. Define the tick function to update positions
    h += "simulation.on('tick', function() {"
    h += "link"
    h += ".attr('x1', d => d.source.x)"
    h += ".attr('y1', d => d.source.y)"
    h += ".attr('x2', d => d.target.x)"
    h += ".attr('y2', d => d.target.y);"  + "\n"

    # Update node positions
    h += "node.attr('cx', d => d.x).attr('cy', d => d.y);"  + "\n"

    # Update label positions
    h += "labels.attr('x', d => d.x).attr('y', d => d.y);"
    h += "});"  + "\n"

    # 9. Drag functions to allow node movement
    h += "function dragStarted(event) {"
    h += "if (!event.active) simulation.alphaTarget(0.3).restart();"
    h += "event.subject.fx = event.subject.x;"
    h += "event.subject.fy = event.subject.y;"
    h += "}"  + "\n"

    h += "function dragged(event) {"
    h += "event.subject.fx = event.x;"
    h += "event.subject.fy = event.y;"
    h += "}"  + "\n"

    h += "function dragEnded(event) {"
    h += "if (!event.active) simulation.alphaTarget(0);"
    h += "event.subject.fx = null;"
    h += "event.subject.fy = null;"
    h += "}"  + "\n"
    h += "</script>"

    h += '</div></div></div>'
    return h

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

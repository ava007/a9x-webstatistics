# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart:
def navchart(d, owndomain, omit):
    h = ''
    links = []    # {'source': 'google.com', 'target': '/team/view/ax', 'c': 1}
    nodes = []    # {'id': 'google.com', 'y':'root'}
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
                    if ('.com' in n[i] or
                           '.ru' in n[i]):
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
                tmplink['cnt'] = 0
                for tdk,tdv in tv['target'].items():
                    if any(oelm in tdk for oelm in omit):  # don not show parts of url 
                        continue
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
    #if len(toplng) > 0:
    if 'logikfabrik' in owndomain:
        h += "\n\n"
        h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
        h += '<div class="card mt-2"><div class="card-body">'
        h += '<h3 class="card-title">Navigation Chart</h3>'
        h += '<p class="card-text">User Navigation Chart for ' + owndomain + ':</p>'
        h += '<div id="navchart-container"><svg id="svgchart" width="600" height="400"></svg></div>'
        h += '<script type="module">' + "\n"
        h += 'const nodes = ' + str(nodes) + ';' + "\n"
        h += 'const links = ' + str(links) + ';' + "\n"
        h += 'const rect = document.getElementById("navchart-container").getBoundingClientRect();'
        h += 'const margin = { top: 20, right: 20, bottom: 40, left: 100 };'
        h += 'const width = Math.round(rect.width) - margin.left - margin.right;'
        #h += 'const height = 400 - margin.top - margin.bottom;'  + "\n"
        h += 'const height = width;'  + "\n"   # make height at least as width

        # 2. Set up the SVG container and set dimensions
        h += 'const svg = d3.select("#svgchart").attr("width", width).attr("height", height);'
       
        # 3. Set up the D3 force simulation
        h += "const simulation = d3.forceSimulation(nodes)"
        h += ".force('link', d3.forceLink(links).id(d => d.id).distance(150))"
        h += ".force('charge', d3.forceManyBody().strength(-300))"
        h += ".force('center', d3.forceCenter(width / 2, height / 2));"  + "\n"

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
        h += ".attr('r', 15)"
        h += ".style('fill','steelblue')"
        h += ".style('stroke','white')"
        h += ".style('stroke-width','1.5px')"
        h += ".call(d3.drag()"
        h += ".on('start', dragStarted)"
        h += ".on('drag', dragged)"
        h += ".on('end', dragEnded));" + "\n"

        # 6. Add labels to the nodes
        h += "const labels = svg.append('g')"
        h += ".selectAll('.label')"
        h += ".data(nodes)"
        h += ".enter().append('text')"
        h += ".style('font-family','Arial, sans-serif')"
        h += ".style('font-size','12px')"
        h += ".style('pointer-events','none')"
        h += ".attr('dx', 25)"
        h += ".attr('dy', '.35em')"
        h += ".text(d => d.name);"  + "\n"

        # 7. Place root nodes along the left side of the screen and freeze their positions
        h += "const rootNodes = nodes.filter(n => n.typ === 'root');"
        h += "rootNodes.forEach((node, index) => {"
        h += "node.x = 100;" # Set all root nodes on the left (x = 100)
        h += "node.y = 100 + index * 100;"   # Distribute vertically along a line
        h += "node.fx = node.x;"  # Freeze position
        h += "node.fy = node.y;"  # Freeze position
        h += "d3.selectAll('.node').filter(d => d.id === node.id).style('fill', 'red');"  # color red
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

        #h += '</p>'
        h += '</div></div></div>'
    return h

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

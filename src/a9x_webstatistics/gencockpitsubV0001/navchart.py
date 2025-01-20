# -*- coding: utf-8 -*-
from operator import itemgetter

# navigation chart:
def navchart(d, owndomain, omit):
    h = ''
    links = []    # {'s': 'google.com', 't': '/team/view/ax', 'c': 1}
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
                # allow only a-z and 0-9:
                if n[0] == '/':    # to avoid empty na
                    n[0] = owndomain
                if n[1] == '/':    # to avoid empty nb
                    n[1] = owndomain
                tmplink = {}
                tmplink['s'] = n[0]
                tmplink['t'] = n[1]
                tmplink['c'] = sv
                duplicate_found = False
                for li in links:
                    if (li['s'] == tmplink['s']
                            and li['t'] == tmplink['t']):
                        duplicate_found = True
                        li['c'] += sv
                        break
                if duplicate_found == False:
                    links.append(tmplink)
                   
                tmpnode = {}
                tmpnode['id'] = n[0]
                if ('.com' in tmpnode['id'] or
                       '.ru' in tmpnode['id']):
                    tmpnode['y'] = 'root'
                duplicate_found = False
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
        h += '<p class="card-text">User Navigation Chart for ' + owndomain + ':'
        h += '<div id="navchart-container"><svg id="svgchart" width="600" height="400"></svg></div>'
        h += '<script type="module">' + "\n"
        h += 'const nodes = ' + str(nodes) + ';' + "\n"
        h += 'const links = ' + str(links) + ';' + "\n"
        h += 'const rect = document.getElementById("navchart-container").getBoundingClientRect();'
        h += 'const margin = { top: 20, right: 20, bottom: 40, left: 100 };'
        h += 'const width = Math.round(rect.width) - margin.left - margin.right;'
        h += 'const height = 400 - margin.top - margin.bottom;'  + "\n"

        # 2. Set up the SVG container and dimensions
        h += 'const svg = d3.select("#svgchart");'
        #h += "const width = +svg.attr('width');"   # duplicate to line 66-67
        #h += "const height = +svg.attr('height');" + "\n"
       
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
        h += ".attr('class', 'link');"  + "\n"

        # 5. Create nodes
        h += "const node = svg.append('g')"
        h += ".selectAll('.node')"
        h += ".data(nodes)"
        h += ".enter().append('circle')"
        h += ".attr('class', 'node')"
        h += ".attr('r', 20)"
        h += ".call(d3.drag()"
        h += ".on('start', dragStarted)"
        h += ".on('drag', dragged)"
        h += ".on('end', dragEnded));" + "\n"

        # 6. Add labels to the nodes
        h += "const labels = svg.append('g')"
        h += ".selectAll('.label')"
        h += ".data(nodes)"
        h += ".enter().append('text')"
        h += ".attr('class', 'label')"
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
        h += "});"  + "\n"

        # 8. Define the tick function to update positions
        h += "simulation.on('tick', function() {"
        # Update link positions
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

        h += '</p>'
        h += '</div></div></div>'
    return h

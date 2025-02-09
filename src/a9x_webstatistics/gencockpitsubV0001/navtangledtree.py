# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart in tangled tree visualization:
def navchartTangledtree(nodes, links, owndomain, omit):

    # const levels = [[{'id': 'start'}], [{'id': 'business', 'parents': ['start']}], [{'id': 'comparison', 'parents': ['start']}]
    levels = [[{'id': 'start', 'name': 'start'}]]
    print("links: " + str(links))

    # append root nodes to levels L1:
    # root nodes are sources that never appear in target
    tmplevel1 = []
    for n1 in nodes:
        found = False
        for l1 in links:
            if l1['target'] == n1['id']:
                found = True
                break
        if found == False:
            tmp = {}
            tmp['id'] = n1['id']
            tmp['name'] = n1['name']
            tmp['parents'] = ['start']
            tmplevel1.append(tmp)
    levels.append(tmplevel1)

    print("levels1: " + str(levels) )

    # 2nd Level:
    tmplevel2 = []
    for l1 in tmplevel1:
        print("l1: " + str(l1))
        found = False
        for li2 in links:
            if li2['source'] == l1['id']:
                found = True
                break
        if found == True:
            # check if l1 is already there --> add to parents
            parent_found = False
            for l2a in tmplevel2:
                if l2a['id'] == li2['target']:
                    parent_found = True
                    l2a['parents'].append(l1['id'])
                    break
            if parent_found == False:
                tmp = {}
                tmp['id'] = li2['target']
                tmp['name'] = li2['target']
                tmp['parents'] = [l1['id']]
                for n2 in nodes:
                    if li2['target'] == n2['id']:
                        tmp['name'] = n2['name']
                        break
                tmplevel2.append(tmp)
            
    levels.append(tmplevel2)

    # 3rd Level:
    tmplevel3 = []
    for l2 in tmplevel2:
        print("l2: " + str(l2))
        found = False
        for li3 in links:
            if li3['source'] == l2['id']:
                found = True
                break
        if found == True:
            # check if l2 is already there --> add to parents
            parent_found = False
            for l3a in tmplevel3:
                if l3a['id'] == li3['target']:
                    parent_found = True
                    l3a['parents'].append(l2['id'])
                    break
            if parent_found == False:
                tmp = {}
                tmp['id'] = li3['target']
                tmp['name'] = li3['target']
                tmp['parents'] = [l2['id']]
                for n3 in nodes:
                    if li3['target'] == n3['id']:
                        tmp['name'] = n3['name']
                        break
                tmplevel3.append(tmp)
            
    levels.append(tmplevel3)
 

    # d3js horizontal bubble char in case results are available
    h = "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
    h += '<div class="card mt-2"><div class="card-body">'
    h += '<h3 class="card-title">Navigation Chart</h3>'
    h += '<p class="card-text">User Navigation Chart for ' + owndomain + ':</p>'
    h += '<div id="navchart-tangledtree-container"></div>'
    h += '<script type="module">' + "\n"
    h += 'const levels = ' + str(levels) + ';' + "\n"
    h += 'const color = d3.scaleOrdinal(d3.schemeDark2);'

    h += 'const rect = document.getElementById("navchart-tangledtree-container").getBoundingClientRect();'
    h += 'const margins = { top: 20, right: 20, bottom: 40, left: 100 };'
    h += 'const width = Math.round(rect.width) - margins.left - margins.right;'
    h += 'const height = width;'  + "\n"   # make height at least as width
    h += 'const totalWidth = width + margins.left + margins.right;'
    h += 'const totalHeight = height + margins.top + margins.bottom;'
    h += 'const svg = d3.select("#navchart-tangledtree-container")'
    h += '.append("svg")'
    h += '.attr("width", totalWidth)'
    h += '.attr("height", totalHeight)'
    h += '.attr("viewBox", [0,0 , totalWidth, totalHeight])' + "\n"
    h += '.attr("style", "max-width: 100%; height: auto; font: 10px sans-serif; height: intrinsic;");' + "\n"

    h += 'const graphGroup = svg.append("g");'
    #h += '.attr("transform", "translate(20," + margins.top + ")");'

    h += 'levels.unshift([]);'

    # We add one pseudo node to every level to deal with parentless nodes
    h += 'levels.forEach((l, i) => {'
    h += 'l.forEach((n, j) => {'
    h += 'n.level = i;'
    h += 'if (n.parents !== undefined) {'
    h += '  n.parent = n.parents[0];'
    h += '} else {'
    h += '  n.parent = `pseudo-${i - 1}`;'
    h += '}'
    h += '});'
    h += 'l.unshift({'
    h += 'id: `pseudo-${i}`,'
    h += 'parent: i > 0 ? `pseudo-${i - 1}` : "",'
    h += 'level: i'
    h += '});'
    h += '});' + "\n"

    h += 'const nodes = levels.flat();'
    h += 'const colours = d3.scaleOrdinal()'
    h += '.domain(nodes.filter(n => n.parents)'
    h += '.map(n => n.parents.sort()'
    h += '.join("-")))'
    h += '.range(d3.schemePaired);'

    h += 'function getLinks(nodes) {'
    h += 'return nodes'
    h += '.filter(n => n.data.parents !== undefined)'
    h += '.map(n => n.data.parents.map(p => ({ source: nodes.find(n => n.id === p), target: n  })))'
    h += '.flat();'
    h += '}'  + "\n"

    h += 'const offsetPerPartner = 3;'
    h += 'const drawNodePath = d => {'
    h += 'const radius = 5;'
    # // The number of partners determines the node height
    # // But when a node has only one partner,
    # // treat it the same as when it has zero
    h += 'const nPartners = (d.data.partners && d.data.partners.length > 1) ? d.data.partners.length : 0;'  + "\n"

    #// We want to centre each node
    h += 'const straightLineOffset = (nPartners * offsetPerPartner) / 2;'

    h += 'const context = d3.path();'
    h += 'context.moveTo(-radius, 0);'
    h += 'context.lineTo(-radius, -straightLineOffset);'
    h += 'context.arc(0, -straightLineOffset, radius, -Math.PI, 0);'
    h += 'context.lineTo(radius, straightLineOffset);'
    h += 'context.arc(0, straightLineOffset, radius, 0, Math.PI);'
    h += 'context.closePath();'

    h += 'return context + "";'
    h += '};' + "\n"

    h += 'const drawLinkCurve = (x0, y0, x1, y1, offset, radius) => {'
    h += 'const context = d3.path();'
    h += 'context.moveTo(x0, y0);'
    h += 'context.lineTo(x1 - 2 * radius - offset, y0);'  + "\n"

    #// If there is not enough space to draw two corners, reduce the corner radius
    h += 'if (Math.abs(y0 - y1) < 2 * radius) { radius = Math.abs(y0 - y1) / 2; }'  + "\n"

    h += 'if (y0 < y1) {'
    h += 'context.arcTo(x1 - offset - radius, y0, x1 - offset - radius, y0 + radius, radius);'
    h += 'context.lineTo(x1 - offset - radius, y1 - radius);'
    h += 'context.arcTo(x1 - offset - radius, y1, x1 - offset, y1, radius);'
    h += '} else if (y0 > y1) {'
    h += 'context.arcTo(x1 - offset - radius, y0, x1 - offset - radius, y0 - radius, radius);'
    h += 'context.lineTo(x1 - offset - radius, y1 + radius);'
    h += 'context.arcTo(x1 - offset - radius, y1, x1 - offset, y1, radius);'
    h += '}' + "\n"
    h += 'context.lineTo(x1, y1);'
    h += 'return context + "";'
    h += '};' + "\n"

    h += 'const partnershipsPerLevel = {};'
    h += 'const getPartnershipOffset = (parent, partner) => {'
    h += 'let partnershipId, level;'
    h += 'if(partner !== undefined) {'
    #// On every level, every relationship gets its own offset. If a relationship
    #// spans multiple levels, the furthest level is chosen
    h += 'level = Math.max(parent.depth, partner.level);'
    h += 'if(!partnershipsPerLevel[level]) { partnershipsPerLevel[level] = []; }'
    h += 'partnershipId = [parent.id, partner.id].sort().join("-");'
    h += '} else {'
    h += 'level = parent.depth;'
    h += 'if(!partnershipsPerLevel[level]) { partnershipsPerLevel[level] = []; }'
    h += 'partnershipId = parent.id;'
    h += '}'

    #// Assume that the partnership already has a slot assigned
    h += 'const partnershipOffset = partnershipsPerLevel[level].indexOf(partnershipId);'
    h += 'if(partnershipOffset === -1) {'
    #// Apparently not
    h += 'return partnershipsPerLevel[level].push(partnershipId) - 1;'
    h += '}'
    h += 'return partnershipOffset;'
    h += '}' + "\n"

    h += 'const lineRadius = 10;'
    h += 'const offsetStep = 5;'
    h += 'const linkFn = link => {'
    h += 'const thisParent = link.source;'
    h += 'const partnerId = link.target.data.parents.find(p => p !== thisParent.id);'
    h += 'const partners = thisParent.data.partners || [];' + "\n"

    #// Let the first link start with this negative offset
    #// But when a node has only one partner,
    #// treat it the same as when it has zero
    h += 'const startOffset = (partners.length > 1) ? -(partners.length * offsetPerPartner) / 2 : 0;'  + "\n"

    h += 'const partner = partners.find(p => p.id === partnerId);'

    # Chaos has no partner, nor Zeus with Athena
    h += 'const nthPartner = partner !== undefined'
    h += '? partners.indexOf(partner)'
    h += ': (partners || []).length;'
    h += 'const partnershipOffset = getPartnershipOffset(thisParent, partner);' + "\n"

    h += 'return drawLinkCurve('
    h += 'thisParent.y,'
    h += 'thisParent.x + startOffset + offsetPerPartner * nthPartner,'
    h += 'link.target.y,'
    h += 'link.target.x,'
    h += 'offsetStep * partnershipOffset,'
    h += 'lineRadius'
    h += ');'
    h += '};' + "\n"

    h += 'function draw(root) {'
    #// Now every node has had it's position set, we can draw them now
    h += 'const nodes = root.descendants().filter(n => !n.id.startsWith("pseudo-"));'
    h += 'const links = getLinks(nodes).filter(l => !l.source.id.startsWith("pseudo-"));'  + "\n"

    h += 'const link = graphGroup.selectAll(".link").data(links);'
    h += 'link.exit().remove();'
    h += 'link.enter()'
    h += '.append("path")'
    h += '.attr("class", "link")'
    h += '.style("fill", "none")'  # from stylesheet
    h += '.merge(link)'
    h += '.attr("stroke", d => colours(d.target.data.parents.sort().join("-")))'
    h += '.attr("d", linkFn);'  + "\n"

    h += 'const node = graphGroup.selectAll(".node").data(nodes);'
    h += 'node.exit().remove();'
    h += 'const newNode = node.enter().append("g")'
    h += '.on("click", click)'
    h += '.attr("class", "node")'
    h += '.append("a")'
    h += '.attr("xlink:href", d => d.data.name ? (d.data.name.startsWith("/") ? `https://'+ owndomain + '${d.data.name}` : `https://${d.data.name}`) : "#")'
    h += '.attr("target", "_blank")' # Opens the link in a new tab
    h += '.attr("title", d => `${d.name}`)'
    h += ';'  + "\n"

    h += 'newNode.append("path").attr("d", drawNodePath);'
    h += 'newNode.append("text")'
    h += '.attr("dy", -3)'
    h += '.attr("x", 6)'
    h += '.style("font-size", "10px")'
    h += '.style("font-family", "sans-serif,Open Sans");'  + "\n"

    h += 'newNode.merge(node)'
    h += '.attr("transform", d => `translate(${d.y},${d.x})`)'
    #h += '.attr("transform", d => `translate(${d.y - width / 2},${d.x})`)'
    h += '.selectAll("text")'
    #h += '.text(d => d.id + (d.cnt ? ` (${d.cnt})` : ""));' # add cnt if available
    h += '.text(d => d.data.name + (d.cnt ? ` (${d.cnt})` : ""));' # add cnt if available
    h += '}' + "\n"

    h += 'const root = d3.stratify().parentId(d => d.parent)(nodes);'  + "\n"

    #// Map the different sets of parents,
    #// assigning each parent an array of partners
    h += 'getLinks(root.descendants())'
    h += '.filter(l => l.target.data.parents)'
    h += '.forEach(l => {'
    h += 'const parentNames = l.target.data.parents;'
    h += 'if (parentNames.length > 1) {'
    h += 'const parentNodes = parentNames.map(p => nodes.find(n => n.id === p));'  + "\n"

    h += 'parentNodes.forEach(p => {'
    h += 'if (!p.partners) {'
    h += 'p.partners = [];'
    h += '}'
    h += 'parentNodes'
    h += '.filter(n => n !== p && !p.partners.includes(n))'
    h += '.forEach(n => { p.partners.push(n); });'
    h += '});'
    h += '}'
    h += '});'  + "\n"

    #// Take nodes with more partners first,
    #// also counting the partners of the children
    h += 'root'
    h += '.sum(d => (d.value || 0) + (d.partners || []).length)'
    h += '.sort((a, b) => b.value - a.value);' + "\n"

    h += 'const tree = d3.tree().size([height, width * 1.2])'
    h += '.separation((a, b) => {'
    #// More separation between nodes with many children
    h += 'const totalPartners = (a.data.partners || []).length + (b.data.partners || []).length;'
    h += 'return 1 + (totalPartners / 5);'
    h += '});' + "\n"

    h += 'draw(tree(root));' + "\n"

    h += 'function collapse(d) {'
    h += 'if (d.children) {'
    h += 'd._children = d.children;'
    h += 'd._children.forEach(collapse);'
    h += 'd.children = null;'
    h += '}'
    h += '}'
    h += 'function click(d) {'
    h += 'if (d.children) {'
    h += 'd._children = d.children;'
    h += 'd.children = null;'
    h += '} else {'
    h += 'd.children = d._children;'
    h += 'd._children = null;'
    h += '}'
    h += 'update(d);'
    h += '} '
    h += "</script>"
    h += '</div></div></div>'
    return h

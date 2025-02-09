# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart in tangled tree visualization:
def navchartTangledtree2(nodes, links, owndomain, omit):

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
    #--------- N E W ----------------------------------------------------
    h += "\n\n"
    h += 'constructTangleLayout = (levels, options={}) => {'
    h += '// precompute level depth'
    h += 'levels.forEach((l, i) => l.forEach(n => (n.level = i)));'
    h += 'var nodes = levels.reduce((a, x) => a.concat(x), []);'
    h += 'var nodes_index = {};'
    h += 'nodes.forEach(d => (nodes_index[d.id] = d));'
    h += '// objectification'
    h += 'nodes.forEach(d => {'
    h += 'd.parents = (d.parents === undefined ? [] : d.parents).map('
    h += '  p => nodes_index[p]'
    h += ');});' + "\n"

    h += '// precompute bundles'
    h += 'levels.forEach((l, i) => {'
    h += 'var index = {};'
    h += 'l.forEach(n => { if (n.parents.length == 0) { return;}'
    h += 'var id = n.parents'
    h += '.map(d => d.id)'
    h += '.sort()'
    h += '.join('-X-');'
    h += 'if (id in index) {'
    h += 'index[id].parents = index[id].parents.concat(n.parents);'
    h += '} else {'
    h += 'index[id] = { id: id, parents: n.parents.slice(), level: i, span: i - d3.min(n.parents, p => p.level) };'
    h += '}'
    h += 'n.bundle = index[id];'
    h += '});'
    h += 'l.bundles = Object.keys(index).map(k => index[k]);'
    h += 'l.bundles.forEach((b, i) => (b.i = i));'
    h += '});'

    h += 'var links = [];'
    h += 'nodes.forEach(d => {'
    h += 'd.parents.forEach(p =>'
    h += 'links.push({ source: d, bundle: d.bundle, target: p })'
    h += ');'
    h += '});'

    h += 'var bundles = levels.reduce((a, x) => a.concat(x.bundles), []);'

    h += '// reverse pointer from parent to bundles'
    h += 'bundles.forEach(b =>'
    h += 'b.parents.forEach(p => {'
    h += 'if (p.bundles_index === undefined) {'
    h += 'p.bundles_index = {};'
    h += '}'
    h += 'if (!(b.id in p.bundles_index)) {'
    h += 'p.bundles_index[b.id] = [];'
    h += '}'
    h += 'p.bundles_index[b.id].push(b);'
    h += '})'
    h += ');'

    h += 'nodes.forEach(n => {'
    h += 'if (n.bundles_index !== undefined) {'
    h += 'n.bundles = Object.keys(n.bundles_index).map(k => n.bundles_index[k]);'
    h += '} else {'
    h += 'n.bundles_index = {};'
    h += 'n.bundles = [];'
    h += '}'
    h += 'n.bundles.sort((a,b) => d3.descending(d3.max(a, d => d.span), d3.max(b, d => d.span)))'
    h += 'n.bundles.forEach((b, i) => (b.i = i));'
    h += '});'

    h += 'links.forEach(l => {'
    h += 'if (l.bundle.links === undefined) {'
    h += 'l.bundle.links = [];'
    h += '}'
    h += 'l.bundle.links.push(l);'
    h += '});'

    h += '// layout'
    h += 'const padding = 8;'
    h += 'const node_height = 22;'
    h += 'const node_width = 70;'
    h += 'const bundle_width = 14;'
    h += 'const level_y_padding = 16;'
    h += 'const metro_d = 4;'
    h += 'const min_family_height = 22;'
  
    h += 'options.c ||= 16;'
    h += 'const c = options.c;'
    h += 'options.bigc ||= node_width+c;'

    h += 'nodes.forEach('
    h += 'n => (n.height = (Math.max(1, n.bundles.length) - 1) * metro_d)'
    h += ');'

    h += 'var x_offset = padding;'
    h += 'var y_offset = padding;'
    h += 'levels.forEach(l => {'
    h += 'x_offset += l.bundles.length * bundle_width;'
    h += 'y_offset += level_y_padding;'
    h += 'l.forEach((n, i) => {'
    h += 'n.x = n.level * node_width + x_offset;'
    h += 'n.y = node_height + y_offset + n.height / 2;'

    h += 'y_offset += node_height + n.height;'
    h += '});'
    h += '});'

    h += 'var i = 0;'
    h += 'levels.forEach(l => {'
    h += 'l.bundles.forEach(b => {'
    h += 'b.x ='
    h += 'd3.max(b.parents, d => d.x) +'
    h += 'node_width +'
    h += '(l.bundles.length - 1 - b.i) * bundle_width;'
    h += 'b.y = i * node_height;'
    h += '});'
    h += 'i += l.length;'
    h += '});'

    h += 'links.forEach(l => {'
    h += 'l.xt = l.target.x;'
    h += 'l.yt ='
    h += 'l.target.y +'
    h += 'l.target.bundles_index[l.bundle.id].i * metro_d -'
    h += '(l.target.bundles.length * metro_d) / 2 +'
    h += 'metro_d / 2;'
    h += 'l.xb = l.bundle.x;'
    h += 'l.yb = l.bundle.y;'
    h += 'l.xs = l.source.x;'
    h += 'l.ys = l.source.y;'
    h += '});'
  
    h += '// compress vertical space'
    h += 'var y_negative_offset = 0;'
    h += 'levels.forEach(l => {'
    h += 'y_negative_offset +='
    h += '-min_family_height +'
    h += 'd3.min(l.bundles, b =>'
    h += 'd3.min(b.links, link => link.ys - 2*c - (link.yt + c))'
    h += ') || 0;'
    h += 'l.forEach(n => (n.y -= y_negative_offset));'
    h += '});'

    h += 'links.forEach(l => {'
    h += 'l.yt ='
    h += 'l.target.y +'
    h += 'l.target.bundles_index[l.bundle.id].i * metro_d -'
    h += '(l.target.bundles.length * metro_d) / 2 +'
    h += 'metro_d / 2;'
    h += 'l.ys = l.source.y;'
    h += 'l.c1 = l.source.level - l.target.level > 1 ? Math.min(options.bigc, l.xb-l.xt, l.yb-l.yt)-c : c;'
    h += 'l.c2 = c;'
    h += '});'

    h += 'var layout = {'
    h += 'width: d3.max(nodes, n => n.x) + node_width + 2 * padding,'
    h += 'height: d3.max(nodes, n => n.y) + node_height / 2 + 2 * padding,'
    h += 'node_height,'
    h += 'node_width,'
    h += 'bundle_width,'
    h += 'level_y_padding,'
    h += 'metro_d'
    h += '};'

    h += 'return { levels, nodes, nodes_index, links, bundles, layout };'
    h += '}'

    h += 'renderChart = (data, options={}) => {'
    h += 'options.color ||= (d, i) => color(i)'
    h += 'const tangleLayout = constructTangleLayout(_.cloneDeep(data), options);'
    h += '  return svg`<svg width="${tangleLayout.layout.width}" height="${'
    h += 'tangleLayout.layout.height'
    h += '}" style="background-color: ${background_color}">'
    h += '<style>'
    h += 'text { font-family: sans-serif; font-size: 10px;}'
    h += '.node { stroke-linecap: round; }'
    h += '.link { fill: none; }'
    h += '</style>'

    h += '${tangleLayout.bundles.map((b, i) => {'
    h += 'let d = b.links'
    h += '.map('
    h += 'l => `'
    h += 'M${l.xt} ${l.yt}'
    h += 'L${l.xb - l.c1} ${l.yt}'
    h += 'A${l.c1} ${l.c1} 90 0 1 ${l.xb} ${l.yt + l.c1}'
    h += 'L${l.xb} ${l.ys - l.c2}'
    h += 'A${l.c2} ${l.c2} 90 0 0 ${l.xb + l.c2} ${l.ys}'
    h += 'L${l.xs} ${l.ys}`'
    h += ').join("");'
    h += 'return `'
    h += '<path class="link" d="${d}" stroke="${background_color}" stroke-width="5"/>'
    h += '<path class="link" d="${d}" stroke="${options.color(b, i)}" stroke-width="2"/>'
    h += '`;'
    h += '})}'
    h += '${tangleLayout.nodes.map('
    h += 'n => `'
    h += '<path class="selectable node" data-id="${'
    h += 'n.id'
    h += '}" stroke="black" stroke-width="8" d="M${n.x} ${n.y - n.height / 2} L${'
    h += 'n.x'
    h += '} ${n.y + n.height / 2}"/>'
    h += '<path class="node" stroke="white" stroke-width="4" d="M${n.x} ${n.y -'
    h += 'n.height / 2} L${n.x} ${n.y + n.height / 2}"/>'
    h += '<text class="selectable" data-id="${n.id}" x="${n.x + 4}" y="${n.y -'
    h += 'n.height / 2 -'
    h += '4}" stroke="${background_color}" stroke-width="2">${n.id}</text>'
    h += '<text x="${n.x + 4}" y="${n.y -'
    h += 'n.height / 2 -'
    h += '4}" style="pointer-events: none;">${n.id}</text>'
    h += '`'
    h += ')}'
    h += '</svg>`;'
    h += '}'

    h += 'renderChart(levels);'
        
    h += "</script>"
    h += '</div></div></div>'
    return h

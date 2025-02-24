# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart in tangled tree visualization:
def navchartTangledtree2(nodes, links, owndomain, omit):

    # const levels = [[{'id': 'start'}], [{'id': 'business', 'parents': ['start']}], [{'id': 'comparison', 'parents': ['start']}]
    levels = [[{'id': 'start', 'name': 'user'}]]
    
    # append root nodes to levels L1:
    # root nodes are sources that never appear in target
    tmplevel1 = []
    i = 0
    for n1 in sorted(nodes, key=itemgetter('co'), reverse=True):
        if any(oelm in n1['name'] for oelm in omit):  # omit parts of url
            continue
        if ':' in n1['id']:   # IP with ports
            continue
        found = False
        for l1 in links:
            if l1['target'] == n1['id']:
                found = True
                break
        if found == False:
            tmp = {}
            tmp['id'] = n1['id']
            tmp['name'] = n1['name'] + " [" + str(n1['co']) + "]"
            tmp['parents'] = ['start']
            tmplevel1.append(tmp)
            i += 1
            if i > 10:
                break
    levels.append(tmplevel1)

    # 2nd Level:
    tmplevel2 = []
    for l1 in tmplevel1:
        found = False
        for li2 in links:
            if li2['source'] == l1['id']:
                if any(oelm in li2['source'] for oelm in omit):  # omit parts of url
                    continue
                if any(oelm in li2['target'] for oelm in omit):  # omit parts of url
                    continue
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
    if len(tmplevel2) > 0:
        levels.append(tmplevel2)

    # 3rd Level:
    tmplevel3 = []
    for l2 in tmplevel2:
        found = False
        for li3 in links:
            if li3['source'] == l2['id']:
                if any(oelm in li2['source'] for oelm in omit):  # omitted parts of url
                    continue
                if any(oelm in li2['target'] for oelm in omit):  # omitted parts of url
                    continue
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
    if len(tmplevel3) > 0:
        levels.append(tmplevel3)

    # 4rd Level:
    tmplevel4 = []
    for l3 in tmplevel3:
        found = False
        for li4 in links:
            if li4['source'] == l3['id']:
                if any(oelm in li2['source'] for oelm in omit):  # omitted parts of url
                    continue
                if any(oelm in li2['target'] for oelm in omit):  # omitted parts of url
                    continue

                # check if l4 is already there --> add to parents
                parent_found = False
                for l4a in tmplevel4:
                    if l4a['id'] == li4['target']:
                        parent_found = True
                        l4a['parents'].append(l3['id'])
                        break
                if parent_found == False:
                    tmp = {}
                    tmp['id'] = li4['target']
                    tmp['name'] = li4['target']
                    tmp['parents'] = [l3['id']]
                    for n4 in nodes:
                        if li4['target'] == n4['id']:
                            tmp['name'] = n4['name']
                            break
                    tmplevel4.append(tmp)
    if len(tmplevel4) > 0:
        levels.append(tmplevel4)

    # d3js horizontal bubble char in case results are available
    h = "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
    h += '<div class="card mt-2"><div class="card-body">'
    h += '<h3 class="card-title">Navigation Chart</h3>'
    h += '<p class="card-text">User Navigation Chart for ' + owndomain + ':</p>'
    h += '<div id="navchart-tangledtree2-container"></div>'
    h += '<script type="module">' + "\n"
    h += 'const levels = ' + str(levels) + ';' + "\n"
    h += 'function renderChart(data, options = {}) {'
    h += 'options.color = options.color || ((d, i) => d3.schemeCategory10[i % 10]);'
            
    h += 'const tangleLayout = constructTangleLayout(JSON.parse(JSON.stringify(data)), options);'
    h += 'const backgroundColor = options.backgroundColor || "#fff";'

    h += 'const rect = document.getElementById("navchart-tangledtree2-container").getBoundingClientRect();'
    h += 'const margins = { top: 20, right: 20, bottom: 40, left: 20 };'
    h += 'const width = Math.round(rect.width) - margins.left - margins.right;'
    h += 'const height = Math.round(width*0.9);'
    h += 'const totalWidth = width + margins.left + margins.right;'
    h += 'const totalHeight = height;'
    h += 'const svg = d3.select("#navchart-tangledtree2-container").append("svg")'
    h += '.attr("id","tt20250216")'
    h += '.attr("width", totalWidth)'
    #h += '.attr("height", totalHeight)'
    h += '.attr("viewBox", [0,0 , totalWidth, totalHeight])'
    h += '.attr("style", "max-width: 100%; font: 10px sans-serif;");' + "\n"

    # M: MoveTo,   L: LineTo,    A: Elliptical arc curve
    h += 'tangleLayout.bundles.forEach((b, i) => {'
    h += 'let d = b.links.map(l => `'
    h += 'M${l.xt} ${l.yt}'
    h += 'L${l.xb - l.c1} ${l.yt}'
    h += 'A${l.c1} ${l.c1} 90 0 1 ${l.xb} ${l.yt + l.c1}'
    h += 'L${l.xb} ${l.ys - l.c2}'
    h += 'A${l.c2} ${l.c2} 90 0 0 ${l.xb + l.c2} ${l.ys}'
    h += 'L${l.xs} ${l.ys}'
    h += '`).join("");'  + "\n"

    h += 'svg.append("path")'
    h += '.attr("class", "link")'
    h += '.attr("d", d)'
    h += '.attr("stroke", options.color(b, i))'
    h += '.attr("stroke-width", 2)'
    h += '.style("fill", "none");'
    h += '});'  + "\n"

    h += 'tangleLayout.nodes.forEach(n => {'
    h += 'svg.append("path")'
    h += '.attr("class", "selectable node")'
    h += '.attr("data-id", n.id)'
    h += '.attr("stroke", "black")'
    h += '.attr("stroke-width", 8)'
    h += '.attr("d", `M${n.x} ${n.y - n.height / 2} L${n.x} ${n.y + n.height / 2}`);'   + "\n"
                
    h += 'svg.append("path")'
    h += '.attr("class", "node")'
    h += '.attr("stroke", "white")'
    h += '.attr("stroke-width", 4)'
    h += '.style("fill", "none")'
    h += '.attr("d", `M${n.x} ${n.y - n.height / 2} L${n.x} ${n.y + n.height / 2}`);'   + "\n"
    
    h += 'const nlink = svg.append("a")'
    h += '.attr("class", "selectable")'
    h += '.attr("data-id", n.id)'
    h += '.attr("xlink:href", d => n.name ? (n.name.startsWith("/") ? `https://'+ owndomain + '${n.name}` : `https://${n.name}`) : "#")'
    h += '.attr("href", n.name ? (n.name.startsWith("/") ? `https://logikfabrik.com${n.name}` : `https://${n.name}`) : "#")'
    h += '.attr("target", "_blank")' 
    h += '.attr("title", d => `${n.name}`);'

    h += 'nlink.append("text")'
    h += '.attr("x", n.x + 4)'
    h += '.attr("y", n.y - n.height / 2 - 4)'
    #h += '.attr("fill", "blue")'
    #h += '.attr("text-decoration", "underline")'
    #h += '.text(n.name);'
    h += '.text(d => {'
    h += '  let lbl;'
    h += '  if (n.name.length > 15) {'
    h += '    lbl = n.name.substring(0,10) + "..." + n.name.slice(-3);'
    h += '  } else {'
    h += '    lbl = n.name;'
    h += '  }'
    h += '  return lbl; }'
    h += ');'  + "\n"
    
    h += '});'
    h += '}'  + "\n"
        
    h += 'function constructTangleLayout(data, options) {'
    # precompute level depth and assign a level for each node:
    h += 'levels.forEach((l, i) => l.forEach(n => (n.level = i)));'

    # nodes will contain all nodes:
    h += 'var nodes = levels.reduce((a, x) => a.concat(x), []);'
    h += 'var nodes_index = {};'
    h += 'nodes.forEach(d => (nodes_index[d.id] = d));'

    # objectification
    h += 'nodes.forEach(d => {'
    h += 'd.parents = (d.parents === undefined ? [] : d.parents).map('
    h += 'p => nodes_index[p]'
    h += ');'
    h += '});'  + "\n"

    # precompute bundles for shared parent relationship:
    h += 'levels.forEach((l, i) => {'
    h += 'var index = {};'
    h += 'l.forEach(n => {'
    h += 'if (n.parents.length == 0) {'
    h += 'return;'
    h += '}'  + "\n"
    h += 'var id = n.parents.map(d => d.id).sort().join("-X-");'
    h += 'if (id in index) {'
    h += 'index[id].parents = index[id].parents.concat(n.parents);'
    h += '} else {'
    h += 'index[id] = { id: id, parents: n.parents.slice(), level: i, span: i - d3.min(n.parents, p => p.level) };'
    h += '}'
    h += 'n.bundle = index[id];'
    h += '});'
    h += 'l.bundles = Object.keys(index).map(k => index[k]);'
    h += 'l.bundles.forEach((b, i) => (b.i = i));'
    h += '});'  + "\n"

    # create links between nodes and parents:
    h += 'var links = [];'
    h += 'nodes.forEach(d => {'
    h += 'd.parents.forEach(p =>'
    h += 'links.push({ source: d, bundle: d.bundle, target: p })'
    h += ');'
    h += '});'  + "\n"

    h += 'var bundles = levels.reduce((a, x) => a.concat(x.bundles), []);'

    # reverse pointer from parent to bundles
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
    h += ');' + "\n"

    h += 'nodes.forEach(n => {'
    h += 'if (n.bundles_index !== undefined) {'
    h += 'n.bundles = Object.keys(n.bundles_index).map(k => n.bundles_index[k]);'
    h += '} else {'
    h += 'n.bundles_index = {};'
    h += 'n.bundles = [];'
    h += '}'
    h += 'n.bundles.sort((a,b) => d3.descending(d3.max(a, d => d.span), d3.max(b, d => d.span)));'
    h += 'n.bundles.forEach((b, i) => (b.i = i));'
    h += '});' + "\n"

    h += 'links.forEach(l => {'
    h += 'if (l.bundle.links === undefined) { l.bundle.links = []; }'
    h += 'l.bundle.links.push(l);'
    h += '});' + "\n"

    # layout
    h += 'const padding = 8;'
    h += 'const node_height = 22;'
    h += 'const node_width = 70;'
    h += 'const bundle_width = 14;'
    h += 'const level_y_padding = 16;'
    h += 'const metro_d = 4;'
    h += 'const min_family_height = 22;'
    h += 'options.c ||= 16;'
    h += 'const c = options.c;'
    h += 'options.bigc ||= node_width+c;' + "\n"

    h += 'nodes.forEach(n => (n.height = (Math.max(1, n.bundles.length) - 1) * metro_d));' + "\n"

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
    h += '});' + "\n"

    h += 'var i = 0;'
    h += 'levels.forEach(l => {'
    h += 'l.bundles.forEach(b => {'
    h += 'b.x = d3.max(b.parents, d => d.x) + node_width +'
    h += '(l.bundles.length - 1 - b.i) * bundle_width;'
    h += 'b.y = i * node_height;'
    h += '});'
    h += 'i += l.length;'
    h += '});' + "\n"

    h += 'links.forEach(l => {'
    h += 'l.xt = l.target.x;'
    h += 'l.yt ='
    h += 'l.target.y +'
    h += 'l.target.bundles_index[l.bundle.id].i * metro_d -'
    h += '(l.target.bundles.length * metro_d) / 2 + metro_d / 2;'
    h += 'l.xb = l.bundle.x;'
    h += 'l.yb = l.bundle.y;'
    h += 'l.xs = l.source.x;'
    h += 'l.ys = l.source.y;'
    h += '});' + "\n"
  
    # compress vertical space
    h += 'var y_negative_offset = 0;'
    h += 'levels.forEach(l => {'
    h += 'y_negative_offset +='
    h += '-min_family_height +'
    h += 'd3.min(l.bundles, b =>'
    h += 'd3.min(b.links, link => link.ys - 2*c - (link.yt + c))'
    h += ') || 0;'
    h += 'l.forEach(n => (n.y -= y_negative_offset));'
    h += '});' + "\n"

    h += 'links.forEach(l => {'
    h += 'l.yt ='
    h += 'l.target.y +'
    h += 'l.target.bundles_index[l.bundle.id].i * metro_d -'
    h += '(l.target.bundles.length * metro_d) / 2 +'
    h += 'metro_d / 2;'
    h += 'l.ys = l.source.y;'
    h += 'l.c1 = l.source.level - l.target.level > 1 ? Math.min(options.bigc, l.xb-l.xt, l.yb-l.yt)-c : c;'
    h += 'l.c2 = c;'
    h += '});' + "\n"

    h += 'var layout = {'
    h += 'width: d3.max(nodes, n => n.x) + node_width + 2 * padding,'
    h += 'height: d3.max(nodes, n => n.y) + node_height / 2 + 2 * padding,'
    h += 'node_height,'
    h += 'node_width,'
    h += 'bundle_width,'
    h += 'level_y_padding,'
    h += 'metro_d'
    h += '};' + "\n"
    h += 'return { levels, nodes, nodes_index, links, bundles, layout };'
    h += '}' + "\n"
    h += 'renderChart(levels, { backgroundColor: "#f8f8f8" });' + "\n"
    h += 'const SVGgroupElement = document.querySelector("#tt20250216");'
    h += 'const bboxGroup = SVGgroupElement.getBBox();'
    #h += 'console.log("width / height bboxGroup: " + bboxGroup.width + " " + bboxGroup.height );'
    h += 'const svg = d3.select("#tt20250216").attr("height",Math.round(bboxGroup.height) + 40 ).attr("width",Math.round(bboxGroup.width) + 10 )'
    h += '.attr("viewBox", [0,0 , Math.round(bboxGroup.width) + 10, Math.round(bboxGroup.height) + 40 ]);'
    
    h += "</script>"
    h += '</div></div></div>' + "\n"
    return h

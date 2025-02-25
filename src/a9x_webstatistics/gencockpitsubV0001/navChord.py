# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart in tangled tree visualization:
def navChord(nodes, links, owndomain, omit):

    # const levels = [[{'id': 'start'}], [{'id': 'business', 'parents': ['start']}], [{'id': 'comparison', 'parents': ['start']}]
    # const data = [{'source': "a", 'target': 'b'}]
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
    h += '<h3 class="card-title">Navigation Chord Diagram</h3>'
    h += '<p class="card-text">User Navigation Chord Chart for ' + owndomain + ':</p>'
    h += '<div id="navchart-chord-container"></div>'
    h += '<script type="module">' + "\n"
    h += 'const levels = ' + str(levels) + ';' + "\n"
    h += 'function renderChart(data, options = {}) {'
    h += 'const rect = document.getElementById("navchart-chord-container").getBoundingClientRect();'
    h += 'const margins = { top: 20, right: 20, bottom: 40, left: 20 };'
    h += 'const width = Math.round(rect.width) - margins.left - margins.right;'
    h += 'const height = Math.round(width*0.9);'
    h += 'const innerRadius = Math.min(width, height) * 0.5 - 90;'
    h += 'const outerRadius = innerRadius + 10;'

    # Compute a dense matrix from the weighted links in data.
    h += 'const names = d3.sort(d3.union(data.map(d => d.source), data.map(d => d.target)));'
    h += 'const index = new Map(names.map((name, i) => [name, i]));'
    h += 'const matrix = Array.from(index, () => new Array(names.length).fill(0));'
    h += 'for (const {source, target, value} of data) matrix[index.get(source)][index.get(target)] += value;'

    h += 'const chord = d3.chordDirected()'
    h += '      .padAngle(10 / innerRadius)'
    h += '.sortSubgroups(d3.descending)'
    h += '.sortChords(d3.descending);'

    h += 'const arc = d3.arc()'
    h += '.innerRadius(innerRadius)'
    h += '.outerRadius(outerRadius);'
     
    h += 'const ribbon = d3.ribbonArrow().radius(innerRadius - 1).padAngle(1 / innerRadius);'
    h += 'const colors = d3.quantize(d3.interpolateRainbow, names.length);'

    h += 'const totalWidth = width + margins.left + margins.right;'
    h += 'const totalHeight = height;'
    h += 'const svg = d3.select("#navchart-tangledtree2-container").append("svg")'
    h += '.attr("id","tt20250225")'
    h += '.attr("width", width)'
    h += '.attr("height", height)'
    h += '.attr("viewBox", [-width / 2, -height / 2, width, height])'
    h += '.attr("style", "width: 100%; height: auto; font: 10px sans-serif;");'

    h += 'const chords = chord(matrix);'

    h += 'const group = svg.append("g").selectAll().data(chords.groups).join("g");'

    h += 'group.append("path").attr("fill", d => colors[d.index]).attr("d", arc);'

    h += 'group.append("text")'
    h += '.each(d => (d.angle = (d.startAngle + d.endAngle) / 2))'
    h += '.attr("dy", "0.35em")'
    h += '.attr("transform", d => `'
    h += 'rotate(${(d.angle * 180 / Math.PI - 90)})'
    h += 'translate(${outerRadius + 5})'
    h += '${d.angle > Math.PI ? "rotate(180)" : ""}'
    h += '`)'
    h += '.attr("text-anchor", d => d.angle > Math.PI ? "end" : null)'
    h += '.text(d => names[d.index]);'

    h += 'group.append("title")'
    h += '.text(d => `${names[d.index]}'
    h += '${d3.sum(chords, c => (c.source.index === d.index) * c.source.value)} outgoing →'
    h += '${d3.sum(chords, c => (c.target.index === d.index) * c.source.value)} incoming ←`);'

    h += 'svg.append("g")'
    h += '.attr("fill-opacity", 0.75)'
    h += '.selectAll()'
    h += '.data(chords)'
    h += '.join("path")'
    h += '.style("mix-blend-mode", "multiply")'
    h += '.attr("fill", d => colors[d.target.index])'
    h += '.attr("d", ribbon)'
    h += '.append("title")'
    h += '.text(d => `${names[d.source.index]} → ${names[d.target.index]} ${d.source.value}`);'

    h += "</script>"
    h += '</div></div></div>' + "\n"
    return h

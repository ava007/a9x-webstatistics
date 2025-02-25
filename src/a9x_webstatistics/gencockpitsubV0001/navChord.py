# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart in chord-dependency diagram:
# https://observablehq.com/@d3/chord-dependency-diagram/2

def navChord(nodes, links, owndomain, omit):
    data = []

    for li in links:
        if any(oelm in li['source'] for oelm in omit):  # omit parts of url
            continue
        if any(oelm in li['target'] for oelm in omit):  # omit parts of url
            continue
        tmp = {}
        tmp['source'] = li['source']
        tmp['target'] = li['target']
        tmp['value'] = li['c']
        data.append(tmp)

    
    # d3js horizontal bubble char in case results are available
    h = "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
    h += '<div class="card mt-2"><div class="card-body">'
    h += '<h3 class="card-title">Navigation Chord Diagram</h3>'
    h += '<p class="card-text">User Navigation Chord Chart for ' + owndomain + ':</p>'
    h += '<div id="navchart-chord-container"></div>'
    h += '<script type="module">' + "\n"
    h += 'const data = ' + str(data) + ';' + "\n"
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

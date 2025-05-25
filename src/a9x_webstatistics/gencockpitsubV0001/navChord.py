# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart in chord-dependency diagram:
# https://observablehq.com/@d3/chord-dependency-diagram/2

def navChord(d, owndomain, omit):
    data = []

    days = 0
    cnt_int = 0
    cnt_ext = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit months or years:
        if len(k) <= 6:
            continue
        days += 1
        if 'nav' in d['v0001']['days'][k]['user']:
            # entries only
            for e in sorted(d['v0001']['days'][k]['user']['nav'], key=itemgetter('c'), reverse=True):
                if 'p' not in e:
                    continue
                if e['c'] < 1:
                    continue
                if any(e['s'].startswith(om) for om in omit):  # omit parts of url
                    continue
                if any(e['t'].startswith(om) for om in omit):  # omit parts of url
                    continue

                if is_valid_ip(e['s']) == True:  # to suppress ip; ip is not a domain anyway    
                    continue
                if '[' in e['s']:    # hack for IPv6 addresses
                    continue
                if ':' in e['s']:    # hack for IPv6 addresses/ports
                    continue

                data,cnt_ext = addLinkChord(data, e, cnt_ext, owndomain)
                if cnt_ext > 30:  # top 30 entries
                    break

             # internal traffic only
            for e in sorted(d['v0001']['days'][k]['user']['nav'], key=itemgetter('c'), reverse=True):
                if 'p' in e:
                    continue
                if any(e['s'].startswith(om) for om in omit):  # omit parts of url
                    continue
                if any(e['t'].startswith(om) for om in omit):  # omit parts of url
                    continue

                data,cnt_int = addLinkChord(data, e, cnt_int, owndomain)
                if cnt_int > 30:  # top 30 entries
                    break
                    
        if days >= 30:
            break
        days += 1

    if len(data) == 0:
        return ''
   
    # d3js horizontal bubble char in case results are available
    h = "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12 pt-4">'
    h += '<h3>Daily User Navigation</h3>'
    h += '<p>Chord diagram showing user navigation for the last ' + str(days) + ' days on ' + owndomain + ':</p>'
    h += '<div id="navchart-chord-container"></div>'
    h += '<script type="module">' + "\n"
    h += 'const data = ' + str(data) + ';' + "\n"
    h += 'function renderChart(data, options = {}) {'
    h += 'const rect = document.getElementById("navchart-chord-container").getBoundingClientRect();'
    h += 'const margins = { top: 20, right: 20, bottom: 40, left: 20 };'
    h += 'const width = Math.round(rect.width) - margins.left - margins.right;'
    h += 'const height = Math.round(width*0.9);'
    h += 'const innerRadius = Math.min(width, height) * 0.5 - 90;'
    h += 'const outerRadius = innerRadius + 10;' + "\n"

    # Compute a dense matrix from the weighted links in data.
    h += 'const names = d3.sort(d3.union(data.map(d => d.source), data.map(d => d.target)));'
    h += 'const index = new Map(names.map((name, i) => [name, i]));'
    h += 'const matrix = Array.from(index, () => new Array(names.length).fill(0));'
    h += 'for (const {source, target, value} of data) matrix[index.get(source)][index.get(target)] += value;' + "\n"

    h += 'const chord = d3.chordDirected().padAngle(10 / innerRadius)'
    h += '.sortSubgroups(d3.descending).sortChords(d3.descending);' + "\n"

    h += 'const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);'
    h += 'const ribbon = d3.ribbonArrow().radius(innerRadius - 1).padAngle(1 / innerRadius);'
    h += 'const colors = d3.quantize(d3.interpolateRainbow, names.length);' + "\n"

    h += 'const totalWidth = width + margins.left + margins.right;'
    h += 'const totalHeight = height;' + "\n"
    h += 'const svg = d3.select("#navchart-chord-container").append("svg")'
    h += '.attr("id","tt20250225")'
    h += '.attr("width", width)'
    h += '.attr("height", height)'
    h += '.attr("viewBox", [-width / 2, -height / 2, width, height])'
    h += '.attr("style", "width: 100%; height: auto; font: 10px sans-serif;");'  + "\n"
    h += 'const chords = chord(matrix);'

    h += 'const group = svg.append("g").selectAll().data(chords.groups).join("g");'
    h += 'group.append("path").attr("fill", d => colors[d.index]).attr("d", arc);' + "\n"

    h += 'group.append("text")'
    h += '.each(d => (d.angle = (d.startAngle + d.endAngle) / 2))'
    h += '.attr("dy", "0.35em")'
    h += '.attr("transform", d => `'
    h += 'rotate(${(d.angle * 180 / Math.PI - 90)})'
    h += 'translate(${outerRadius + 5})'
    h += '${d.angle > Math.PI ? "rotate(180)" : ""}'
    h += '`)'
    h += '.attr("text-anchor", d => d.angle > Math.PI ? "end" : null)'
    h += '.text(d => names[d.index]);'  + "\n"

    h += 'group.append("title")'
    h += '.text(d => `${names[d.index]}'
    h += '${d3.sum(chords, c => (c.source.index === d.index) * c.source.value)} outgoing →'
    h += '${d3.sum(chords, c => (c.target.index === d.index) * c.source.value)} incoming ←`);' + "\n"

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
    h += '}' + "\n"
    h += 'renderChart(data, { backgroundColor: "#f8f8f8" });' + "\n"
    h += "</script>"
    h += '</div>' + "\n"
    return h
    
def addLinkChord(data, e, cnt, owndomain):
    tmplink = {}
    tmplink['source'] = e['s']
    if tmplink['source'] == '/' or tmplink['source'] == None or tmplink['source'] == '':
        tmplink['source'] = owndomain
                    
    tmplink['target'] = e['t']
    if tmplink['target'] == '/' or tmplink['target'] == None or tmplink['target'] == '':
        tmplink['target'] = owndomain
                    
    tmplink['value'] = e['c']
    if tmplink['source'] == tmplink['target']:
       return data, cnt
                
    duplicate_found = False
    for li in data:
        if (li['source'] == tmplink['source']
            and li['target'] == tmplink['target']):
            duplicate_found = True
            li['value'] += tmplink['value']
            break
    if duplicate_found == False:
        data.append(tmplink)
        cnt += 1
    return data, cnt

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart in chord-dependency diagram:
# https://observablehq.com/@d3/chord-dependency-diagram/2
# https://observablehq.com/@d3/stacked-bar-chart/2

def dailyHitsVisitsChart(d, owndomain, omit):
    rdata = []
    sdata = []
    vdata = []
    days = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit months or years:
        if len(k) <= 6:
            continue
        if days >= 31:
            break
        days += 1
        if 'desktop' in d['v0001']['days'][k]['user']['deviceHits']:
            sdata.append({'d': k, 't': 'desk', 'c': d['v0001']['days'][k]['user']['deviceHits']['desktop']})
        else:
            sdata.append({'d': k, 't': 'desk', 'c': 0})
        if 'mobile' in d['v0001']['days'][k]['user']['deviceHits']:
            sdata.append({'d': k, 't': 'mob', 'c': d['v0001']['days'][k]['user']['deviceHits']['mobile']})
        else:
            sdata.append({'d': k, 't': 'mob', 'c': 0})
        if 'tablet' in d['v0001']['days'][k]['user']['deviceHits']:
            sdata.append({'d': k, 't': 'tab', 'c': d['v0001']['days'][k]['user']['deviceHits']['tablet']})
        else:
            sdata.append({'d': k, 't': 'tab', 'c': 0})

        # visits:
        if 'visits' in d['v0001']['days'][k]['user']:
            vdata.append({'d': k, 'c': d['v0001']['days'][k]['user']['visits']})
        else:
            vdata.append({'d': k, 'c': 0})

        # robots
        if 'robotHits' in d['v0001']['days'][k]['robot']:
            rdata.append({'d': k, 'c': d['v0001']['days'][k]['robot']['robotHits']})
        else:
            rdata.append({'d': k, 'c': 0})
        
    #https://stackoverflow.com/questions/36435384/d3-js-combining-bar-and-line-chart#36435663
   
    # d3js horizontal bubble char in case results are available
    h = "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
    h += '<h3>User Hits and Visits</h3>'
    h += '<p>User hits and visits for the last ' + str(days) + ' days on ' + owndomain + ':</p>'
    h += '<div id="dhvchart-container"></div>'
    h += '<script type="module">' + "\n"
    h += 'const sdata = ' + str(sdata) + ';' + "\n"
    h += 'const vdata = ' + str(vdata) + ';' + "\n"
    h += 'const rdata = ' + str(rdata) + ';' + "\n"

    h += 'const groupedData = d3.rollup(sdata, v => Object.fromEntries(v.map(d => [d.t, d.c])),d => d.d);'

    # Convert to array with missing categories filled as 0
    h += 'const dates = Array.from(groupedData.keys()).sort();'
    h += 'const categories = ["desk", "mob", "tab"];'

    h += 'const transformedData = dates.map(d => {'
    h += 'let entry = { d };'
    h += 'let values = groupedData.get(d) || {};'  # Ensure it's always an object
    h += 'categories.forEach(c => entry[c] = values[c] ?? 0);'  # Use Nullish coalescing to handle undefined
    h += 'return entry;'
    h += '});'

    #// Stack generator
    h += 'const stack = d3.stack().keys(categories);'
    h += 'const series = stack(transformedData);'
    
    # getting max from series,vdata and sdata:
    h += 'const yMax = Math.max('
    h += 'd3.max(series, d => d3.max(d, d => d[1])),'
    h += 'd3.max(vdata, d => d.c),'
    h += 'd3.max(rdata, d => d.c)'
    h += ');' + "\n"
    
    h += 'const container = document.getElementById("dhvchart-container");'
    h += 'const { width } = container.getBoundingClientRect();'
    h += 'const height = width * 0.5;' + "\n"

    h += 'const margins = { top: 20, right: 20, bottom: 50, left: 40 };'
    h += 'const x = d3.scaleBand().domain(dates).range([margins.left, width - margins.right]).padding(0.1);'  + "\n"
    
    #h += 'const y = d3.scaleLinear()'
    #h += '.domain([0, yMax])'
    #h += '.range([height - margins.bottom, margins.top]);'

    h += 'const y = d3.scaleSymlog()'
    h += '.domain([0.1, yMax])'   # Log scale cannot have 0
    h += '.range([height - margins.bottom, margins.top])'
    h += '.nice();'  + "\n"

    h += 'const color = d3.scaleOrdinal().domain(categories).range(["#42f5aa", "#42c5f5", "#f5a742"]);' + "\n"

    h += 'const svg = d3.select("#dhvchart-container")'
    h += '.append("svg")'
    h += '.attr("width", width)'
    h += '.attr("height", height)'
    h += '.attr("viewBox", [0, 0, width, height]);' + "\n"

    # Add bars
    h += 'svg.append("g")'
    h += '.selectAll("g")'
    h += '.data(series)'
    h += '.join("g")'
    h += '.attr("fill", d => color(d.key))'
    h += '.selectAll("rect")'
    h += '.data(d => d)'
    h += '.join("rect")'
    h += '.attr("x", d => x(d.data.d))'
    h += '.attr("y", d => y(Math.max(1, isNaN(d[1]) ? 1 : d[1])))'
    h += '.attr("height", d => Math.max(0, Math.abs(y(d[0]) - y(d[1]))))'
    h += '.attr("width", x.bandwidth());' + "\n"

    h += 'const visitline = d3.line()'
    h += '.x(d => x(d.d) + x.bandwidth()/2 )'
    h += '.y(d => y(d.c));' + "\n"

    # Visits
    h += 'svg.append("path")'
    h += '.datum(vdata)' # Bind data properly
    h += '.attr("fill", "none")'
    h += '.attr("stroke", "red")'
    h += '.attr("stroke-width", 2)'
    h += '.attr("d", visitline);' + "\n"

    # Robots
    h += 'svg.append("path")'
    h += '.datum(rdata)' # Bind data properly
    h += '.attr("fill", "none")'
    h += '.attr("stroke", "grey")'
    h += '.attr("stroke-width", 2)'
    h += '.attr("d", visitline);' + "\n"

    # X-Axis
    h += 'svg.append("g")'
    h += '.attr("transform", `translate(0,${height - margins.bottom})`)'
    h += '.call(d3.axisBottom(x).tickSizeOuter(0))'
    h += '.selectAll("text")'
    h += '.attr("transform", "rotate(45)")'
    h += '.style("text-anchor", "start");' + "\n"

    # Y-Axis
    h += 'svg.append("g")'
    h += '.attr("transform", `translate(${margins.left},0)`)'
    h += '.call(d3.axisLeft(y).ticks(5));' + "\n"

    #h += 'console.log("Transformed Data:", transformedData);'
    #h += 'console.log("Stacked Data:", stack(transformedData));'
    h += "</script>"
    h += '</div>' + "\n"
    return h

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
    h += 'categories.forEach(c => entry[c] = groupedData.get(d)?.[c] || 0);'
    h += 'return entry;'
    h += '});'

    #// Stack generator
    h += 'const stack = d3.stack().keys(categories);'
    h += 'const series = stack(transformedData);'

    h += 'const container = document.getElementById("dhvchart-container");'
    h += 'const { width } = container.getBoundingClientRect();'
    h += 'const height = width * 0.5;'

    h += 'const margins = { top: 20, right: 20, bottom: 50, left: 40 };'
    h += 'const x = d3.scaleBand().domain(dates).range([margins.left, width - margins.right]).padding(0.1);'
    h += 'const y = d3.scaleLinear()'
    h += '.domain([0, d3.max(series, d => d3.max(d, d => d[1]))])'
    h += '.range([height - margins.bottom, margins.top]);'

    h += 'const color = d3.scaleOrdinal().domain(categories).range(["#1f77b4", "#ff7f0e", "#2ca02c"]);'

    h += 'const svg = d3.select("#dhvchart-container")'
    h += '.append("svg")'
    h += '.attr("width", width)'
    h += '.attr("height", height)'
    h += '.attr("viewBox", [0, 0, width, height]);'

    #// Add bars
    h += 'svg.append("g")'
    h += '.selectAll("g")'
    h += '.data(series)'
    h += '.join("g")'
    h += '.attr("fill", d => color(d.key))'
    h += '.selectAll("rect")'
    h += '.data(d => d)'
    h += '.join("rect")'
    h += '.attr("x", d => x(d.data.d))'
    h += '.attr("y", d => y(d[1]))'
    h += '.attr("height", d => y(d[0]) - y(d[1]))'
    h += '.attr("width", x.bandwidth());'

    #// X-Axis
    h += 'svg.append("g")'
    h += '.attr("transform", `translate(0,${height - margins.bottom})`)'
    h += '.call(d3.axisBottom(x).tickSizeOuter(0))'
    h += '.selectAll("text")'
    h += '.attr("transform", "rotate(45)")'
    h += '.style("text-anchor", "start");'

    #// Y-Axis
    h += 'svg.append("g")'
    h += '.attr("transform", `translate(${margins.left},0)`)'
    h += '.call(d3.axisLeft(y).ticks(5));'



    '''
    h += 'function renderChart(data, options = {}) {'
    h += 'const rect = document.getElementById("dhvchart-container").getBoundingClientRect();'
    h += 'const margins = { top: 20, right: 20, bottom: 40, left: 20 };'
    h += 'const width = Math.round(rect.width) - margins.left - margins.right;'
    #h += 'const height = rect.height;' + "\n"
    h += 'const height = width * 0.5;' + "\n"

    # Determine the series that need to be stacked.
    h += 'const series = d3.stack()'
    h += '.keys(d3.union(sdata.map(d => d.t)))'    # distinct series keys, in input order
    h += '.value(([, D], key) => D.get(key).c)'    # get value for each series key and stack
    h += '(d3.index(sdata, d => d.d, d => d.t));' + "\n"  # group by stack then series key

    # Prepare the scales for positional and color encodings.
    h += 'const x = d3.scaleBand()'
    h += '.domain(d3.groupSort(sdata, D => d3.sum(D, d => d.c), d => d.d))'
    h += '.range([margins.left, width - margins.right])'
    h += '.padding(0.1);'  + "\n"

    # getting maxx from series,vdata and sdata:
    h += 'const yMax = Math.max('
    h += 'd3.max(series, d => d3.max(d, d => d[1])),'
    h += 'd3.max(vdata, d => d.c),'
    h += 'd3.max(rdata, d => d.c)'
    h += ');' + "\n"
    
    h += 'const y = d3.scaleLog()'
    h += '.domain([1, yMax])'
    h += '.range([height - margins.bottom, margins.top])'
    h += '.nice();'  + "\n"

    #h += 'const color = d3.scaleOrdinal()'
    #h += '.domain(series.map(d => d.key))'
    #h += '.range(d3.schemeSpectral[series.length])'
    #h += '.unknown("#ccc");'  + "\n"

    h += 'const color = d3.scaleOrdinal()'
    h += '.domain(["desk", "mob", "tab"])'
    h += '.range(["#1f77b4", "#ff7f0e", "#2ca02c"]);' + "\n" # Blue for desk, orange for mobile, green for tablet

    h += 'const visitline = d3.line()'
    h += '.x(d => x(d.d) + x.bandwidth()/2 )'
    h += '.y(d => y(d.c));'

    # A function to format the value in the tooltip.
    h += 'const formatValue = x => isNaN(x) ? "N/A" : x.toLocaleString("en");'

    h += 'const totalWidth = width + margins.left + margins.right;'
    h += 'const svg = d3.select("#dhvchart-container").append("svg")'
    h += '.attr("id","tt20250303")'
    h += '.attr("width", width)'
    h += '.attr("height", height)'
    h += '.attr("viewBox", [0, 0, width, height])'
    h += '.attr("style", "width: 100%; height: auto; font: 10px sans-serif;");'  + "\n"

    # Append a group for each series, and a rect for each element in the series.
    h += 'svg.append("g")'
    h += '.selectAll()'
    h += '.data(series)'
    h += '.join("g")'
    h += '.attr("fill", d => color(d.key))'
    h += '.selectAll("rect")'
    h += '.data(D => D.map(d => (d.key = D.key, d)))'
    h += '.join("rect")'
    h += '.attr("x", d => x(d.data[0]))'
    h += '.attr("y", d => y(d[1]))'
    h += '.attr("height", d => y(d[0]) - y(d[1]))'
    h += '.attr("width", x.bandwidth())'
    h += '.append("title")'
    h += '.text(d => `${d.data[0]} ${d.key}\n${formatValue(d.data[1].get(d.key).c)}`);' + "\n"

    # Append the horizontal axis.
    h += 'svg.append("g")'
    h += '.attr("transform", `translate(0,${height - margins.bottom})`)'
    h += '.call(d3.axisBottom(x).tickSizeOuter(0))'
    h += '.call(g => g.selectAll(".domain").remove())'
    h += '.selectAll("text")'   # Select axis labels
    h += '.attr("transform", "rotate(45)")'  # Rotate text 45 degrees
    h += '.style("text-anchor", "start")'  # Adjust alignment
    h += '.attr("x", 10)'   # Fine-tune position
    h += '.attr("y", 5);' + "\n"

    # Append the vertical axis.
    h += 'svg.append("g")'
    h += '.attr("transform", `translate(${margins.left},0)`)'
    h += '.call(d3.axisLeft(y).ticks(5,",.0f"))'  # format number for log scale
    h += '.call(g => g.selectAll(".domain").remove());' + "\n"

    h += 'svg.append("path")'
    h += '.datum(vdata)' # Bind data properly
    h += '.attr("fill", "none")'
    h += '.attr("stroke", "red")'
    h += '.attr("stroke-width", 2)'
    h += '.attr("d", visitline);' + "\n"

    h += 'svg.append("path")'
    h += '.datum(rdata)' # Bind data properly
    h += '.attr("fill", "none")'
    h += '.attr("stroke", "grey")'
    h += '.attr("stroke-width", 2)'
    h += '.attr("d", visitline);' + "\n"
        
    h += '}' + "\n"
    h += 'renderChart(sdata, { backgroundColor: "#f8f8f8" });' + "\n"
    '''
    h += "</script>"
    h += '</div>' + "\n"
    return h

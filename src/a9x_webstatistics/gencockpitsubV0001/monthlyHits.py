# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

def monthlyHitsVisitsChart(d, owndomain, omit):
    rdata = []
    sdata = []
    vdata = []
    mcount = 0
    startPeriod = None
    endPeriod = None
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit days:
        if len(k) > 6:
            continue
        if mcount > 31:
            break
        mcount += 1
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

        # record start / end period to be displayed on chart:
        if startPeriod is None or k < startPeriod:
            startPeriod = k
        if endPeriod is None:
            endPeriod = k

    # first run / first day:
    if len(sdata) == 0):
        return ''
        
    # d3js horizontal bubble char in case results are available
    h = "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12 pt-4">'
    h += '<h3>User Hits and Visits - Long Term</h3>'
    h += '<p>User hits and visits on ' + owndomain + ' from ' + startPeriod + ' to ' + endPeriod + ':</p>'
    h += '<div id="mhvchart-container"></div>' + "\n"
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

    # Sort the categories within each date by count in ascending order
    h += 'transformedData.forEach(entry => {'
    h += 'const sortedCategories = categories.slice().sort((a, b) => entry[a] - entry[b]);'
    h += 'const sortedEntry = {};'
    h += 'sortedCategories.forEach(c => sortedEntry[c] = entry[c]);'
    h += 'Object.assign(entry, sortedEntry);'
    h += '});'

    # Stack generator
    h += 'const stack = d3.stack().keys(categories);'
    h += 'const series = stack(transformedData);'
    
    # getting max from series,vdata and sdata:
    h += 'const yMax = Math.max('
    h += 'd3.max(series, d => d3.max(d, d => d[1])),'
    h += 'd3.max(vdata, d => d.c),'
    h += 'd3.max(rdata, d => d.c)'
    h += ');' + "\n"
    
    h += 'const container = document.getElementById("mhvchart-container");'
    h += 'const { width } = container.getBoundingClientRect();'
    h += 'const height = width * 0.5;' + "\n"

    h += 'const margins = { top: 20, right: 20, bottom: 50, left: 40 };'
    h += 'const x = d3.scaleBand().domain(dates).range([margins.left, width - margins.right]).padding(0.1);'  + "\n"

    h += 'const y = d3.scaleSymlog()'
    h += '.domain([0.1, yMax])'   # Log scale cannot have 0
    h += '.range([height - margins.bottom, margins.top])'
    h += '.nice();'  + "\n"

    h += 'const color = d3.scaleOrdinal().domain(categories).range(["#42c5f5", "#42f5aa", "#f5a742"]);' + "\n"

    h += 'const svg = d3.select("#mhvchart-container")'
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
    h += '.attr("stroke", "lightgrey")'
    h += '.attr("stroke-width", 2)'
    h += '.attr("d", visitline);' + "\n"

    # Function to add points to a line
    h += 'function addPoints(data, color) {'
    h += 'svg.selectAll(`.point-${color}`)'
    h += '.data(data)'
    h += '.enter()'
    h += '.append("circle")'
    h += '.attr("cx", d => x(d.d) + x.bandwidth() / 2)'
    h += '.attr("cy", d => y(d.c))'
    h += '.attr("r", 4)' # Adjust size of the points
    h += '.attr("fill", color)'
    h += '.attr("stroke", "white")'
    h += '.attr("stroke-width", 1);'
    h += '}'

    # Add points to the red and grey lines
    h += 'addPoints(vdata, "red");'
    h += 'addPoints(rdata, "lightgrey");' + "\n"

    # X-Axis
    h += 'svg.append("g")'
    h += '.attr("transform", `translate(0,${height - margins.bottom})`)'
    h += '.call(d3.axisBottom(x).tickSizeOuter(0))'
    h += '.selectAll("text")'
    h += '.attr("transform", "rotate(45)")'
    h += '.style("text-anchor", "start");' + "\n"

    # Customize y-axis ticks and labels
    h += 'const yAxis = d3.axisLeft(y)'
    h += '.ticks(12)'  # Specify the number of ticks you want
    h += '.tickFormat(d => `${d} units`);' + "\n" #  Format the labels to include "units"

    # Y-Axis
    h += 'svg.append("g")'
    h += '.attr("transform", `translate(${margins.left},0)`)'
    h += '.call(d3.axisLeft(y).ticks(5));' + "\n"

    # Create a tooltip div
    h += 'const tooltip = d3.select("#mhvchart-container")'
    h += '.append("div")'
    h += '.style("position", "absolute")'
    h += '.style("background", "white")'
    h += '.style("padding", "5px")'
    h += '.style("border", "1px solid black")'
    h += '.style("border-radius", "5px")'
    h += '.style("visibility", "hidden")'
    h += '.style("pointer-events", "none");' + "\n"

    # Add tooltip functionality to bars
    h += 'svg.selectAll("rect")'
    h += '.on("mouseover", (event, d) => { tooltip.style("visibility", "visible"); })'
    h += '.on("mousemove", (event, d) => {'
    h += 'tooltip.html(`Date: ${d.data.d}<br>Category: ${d3.select(event.target.parentNode).datum().key}<br>Count: ${d[1] - d[0]}`)'
    h += '.style("top", `${event.pageY - 10}px`)'
    h += '.style("left", `${event.pageX + 10}px`);'
    h += '})'
    h += '.on("mouseleave", () => { tooltip.style("visibility", "hidden"); });' + "\n"

    # Add legend
    h += 'const legend = svg.append("g")'
    h += '.attr("transform", `translate(${width / 2}, 20)`);' + "\n" # Position at the top center

    h += 'const legendItem = legend.selectAll(".legend-item")'
    h += '.data(categories)'
    h += '.enter().append("g")'
    h += '.attr("class", "legend-item")'
    h += '.attr("transform", (d, i) => `translate(${i * 100},0)`);' + "\n" # Arrange horizontally

    h += 'legendItem.append("rect")'
    h += '.attr("width", 18)'
    h += '.attr("height", 18)'
    h += '.attr("fill", d => color(d));'

    h += 'legendItem.append("text")'
    h += '.attr("x", 24)'
    h += '.attr("y", 9)'
    h += '.attr("dy", "0.35em")'
    h += '.text(d => d);'
    
    h += 'console.log("Transformed Data:", transformedData);'
    h += 'console.log("Stacked Data:", stack(transformedData));'
    h += "</script>"
    h += '</div>' + "\n"
    return h

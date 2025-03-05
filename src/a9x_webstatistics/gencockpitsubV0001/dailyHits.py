# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart in chord-dependency diagram:
# https://observablehq.com/@d3/chord-dependency-diagram/2
# https://observablehq.com/@d3/stacked-bar-chart/2

def dailyHitsVisitsChart(d, owndomain, omit):
    sdata = []

    days = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit months or years:
        if len(k) <= 6:
            continue
        if days >= 31:
            break
        days += 1
        day_lbl.append(k)
        tmp = {}
        if 'desktop' in d['v0001']['days'][k]['user']['deviceHits']:
            sdata.append({'d': k, 't': 'desk', 'c': d['v0001']['days'][k]['user']['deviceHits']['desktop']})
        if 'mobile' in d['v0001']['days'][k]['user']['deviceHits']:
            sdata.append({'d': k, 't': 'mob', 'c': d['v0001']['days'][k]['user']['deviceHits']['mobile']})
         if 'tablet' in d['v0001']['days'][k]['user']['deviceHits']:
            sdata.append({'d': k, 't': 'tab', 'c': d['v0001']['days'][k]['user']['deviceHits']['tablet']})
        if 'robotHits' in d['v0001']['days'][k]['robot']:
            day_robot_hits.append(d['v0001']['days'][k]['robot']['robotHits'])
        else:
            day_robot_hits.append(0)

    #https://stackoverflow.com/questions/36435384/d3-js-combining-bar-and-line-chart#36435663
   
    # d3js horizontal bubble char in case results are available
    h = "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
    h += '<div class="card mt-2"><div class="card-body">'
    h += '<h3 class="card-title">User Hits and Visits</h3>'
    h += '<p class="card-text">User hits and visits for the last ' + str(days) + ' days on ' + owndomain + ':</p>'
    h += '<div id="dhvchart-container"></div>'
    h += '<script type="module">' + "\n"
    h += 'const sdata = ' + str(sdata) + ';' + "\n"
    h += 'function renderChart(data, options = {}) {'
    h += 'const rect = document.getElementById("dhvchart-container").getBoundingClientRect();'
    h += 'const margins = { top: 20, right: 20, bottom: 40, left: 20 };'
    h += 'const width = Math.round(rect.width) - margins.left - margins.right;'

    # Determine the series that need to be stacked.
    h += 'const series = d3.stack()'
    h += '.keys(d3.union(sdata.map(d => d.t)))'    # distinct series keys, in input order
    h += '.value(([, D], key) => D.get(key).c)'    # get value for each series key and stack
    h += '(d3.index(sdata, d => d.d, d => d.t));' + "\n"  # group by stack then series key

    # Prepare the scales for positional and color encodings.
    h += 'const x = d3.scaleBand()'
    h += '.domain(d3.groupSort(sdata, D => -d3.sum(D, d => d.c), d => d.d))'
    h += '.range([margins.left, width - margins.right])'
    h += '.padding(0.1);'  + "\n"

    h += 'const y = d3.scaleLinear()'
    h += '.domain([0, d3.max(series, d => d3.max(d, d => d[1]))])'
    h += '.rangeRound([height - margins.bottom, margins.top]);'  + "\n"

    h += 'const color = d3.scaleOrdinal()'
    h += '.domain(series.map(d => d.key))'
    h += '.range(d3.schemeSpectral[series.length])'
    h += '.unknown("#ccc");'  + "\n"

    #// A function to format the value in the tooltip.
    h += 'const formatValue = x => isNaN(x) ? "N/A" : x.toLocaleString("en");'

    h += 'const totalWidth = width + margins.left + margins.right;'
    h += 'const height = rect.height;' + "\n"
    h += 'const svg = d3.select("#dhvchart-container").append("svg")'
    h += '.attr("id","tt20250303")'
    h += '.attr("width", width)'
    h += '.attr("height", height)'
    h += '.attr("viewBox", [-width / 2, -height / 2, width, height])'
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
    h += '.call(g => g.selectAll(".domain").remove());' + "\n"

    # Append the vertical axis.
    h += 'svg.append("g")'
    h += '.attr("transform", `translate(${margins.left},0)`)'
    h += '.call(d3.axisLeft(y).ticks(null, "s"))'
    h += '.call(g => g.selectAll(".domain").remove());' + "\n"

    h += '}' + "\n"
    h += 'renderChart(sdata, { backgroundColor: "#f8f8f8" });' + "\n"
    h += "</script>"
    h += '</div></div></div>' + "\n"
    return h

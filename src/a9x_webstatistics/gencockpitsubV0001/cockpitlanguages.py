# -*- coding: utf-8 -*-
import json
from operator import itemgetter

# top languages for the last 31 days:
def cockpitLanguages(d, owndomain):
    
    # accumulate the results for maximum the last 31 days:
    toplng = {}
    toplngcnt = 0
    total_languages = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # dont take months in account:
        if len(k) <= 6:
            continue
        if toplngcnt >= 31:
            break
        toplngcnt += 1
        if 'language' in d['v0001']['days'][k]['user']:
            for tk, tv in d['v0001']['days'][k]['user']['language'].items():
                if tk not in toplng:
                    toplng[tk] = 0
                toplng[tk] += tv
                total_languages += tv

    # build array for plot:
    language_array = []
    for k, v in sorted(toplng.items(), key=itemgetter(1), reverse=True):
        l = {}
        l['lang'] = k
        l['freq'] = v / total_languages * 100
        if l['freq'] > 0.4:
            language_array.append(l)
                
    h = ''
    # d3js horizontal bubble char in case results are available:
    if len(toplng) > 0:
        h += "\n\n"
        h += '<div class="col-md-12 col-lg-12 col-xxl-12 pt-4">'
        h += '<h3>Top Browser Languages</h3>'
        h += '<p>Webbrowser languages for the last ' + str(toplngcnt) + ' days by based on user hits  on ' + owndomain + ':</p>'
        h += '<div id="browserlanguages-container"><svg id="svglng" width="600" height="400"></svg></div>'
        h += '<script type="module">'
        h += 'const languages = ' + str(language_array) + ';'
        h += 'const rect = document.getElementById("browserlanguages-container").getBoundingClientRect();'
        h += 'const margin = { top: 20, right: 20, bottom: 40, left: 100 };'
        h += 'const width = Math.round(rect.width) - margin.left - margin.right;'
        h += 'const height = 400 - margin.top - margin.bottom;'

        # Create SVG container
        h += 'const svg = d3.select("#svglng")'
        h += '  .attr("width", width + margin.left + margin.right)'
        h += '  .attr("height", height + margin.top + margin.bottom)'
        h += '  .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif; height: intrinsic;")'
        h += '  .append("g")'
        h += '  .attr("transform", `translate(${margin.left}, ${margin.top})`);'

        # Set up the x and y scales
        h += 'const x = d3.scaleLinear()'
        h += '  .domain([0, d3.max(languages, d => d.freq)])'
        h += '  .range([0, width]);'

        h += 'const y = d3.scaleBand()'
        h += '  .domain(languages.map(d => d.lang))'
        h += '  .range([0, height])'
        h += '  .padding(0.1);'

        # Append bars
        h += 'svg.selectAll(".bar")'
        h += '  .data(languages)'
        h += '  .enter().append("rect")'
        h += '  .attr("class", "bar")'
        h += '  .attr("x", 0)'
        h += '  .attr("y", d => y(d.lang))'
        h += '  .attr("width", d => x(d.freq))'
        h += '  .attr("height", y.bandwidth())'
        h += '  .style("fill", "steelblue");'

        # Add labels for percentages
        h += 'svg.selectAll(".label")'
        h += '  .data(languages)'
        h += '  .enter().append("text")'
        h += '  .attr("class", "label")'
        h += '  .attr("x", d => x(d.freq) - 5)'
        h += '  .attr("y", d => y(d.lang) + y.bandwidth() / 2)'
        h += '  .attr("dy", ".35em")'
        h += '  .attr("text-anchor", "end")'
        h += '  .style("fill", "white")'
        h += '  .text(d => d3.format(".1f")(d.freq) + "%");'

        # Add y-axis labels
        h += 'svg.append("g").selectAll(".axis-label")'
        h += '  .data(languages)'
        h += '  .enter().append("text")'
        h += '  .attr("class", "axis-label")'
        h += '  .attr("x", -10)'
        h += '  .attr("y", d => y(d.lang) + y.bandwidth() / 2)'
        h += '  .attr("dy", ".35em")'
        h += '  .attr("text-anchor", "end")'
        h += '  .text(d => d.lang);'
        h += '</script>'
        h += '</div>'  + "\n" 
    return h

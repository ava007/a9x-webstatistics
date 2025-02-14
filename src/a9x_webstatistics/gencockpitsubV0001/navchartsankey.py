# -*- coding: utf-8 -*-
from operator import itemgetter
import ipaddress

# navigation chart as sankey diagram:
def navchartsankey(nodes, links, owndomain, omit):

    # links = []    # {'source': 'google.com', 'target': '/team/view/ax', 'c': 1}
    # nodes = []    # {'id': 'google.com', 'value':1}
 
    # d3js horizontal bubble char in case results are available:
    h = "\n\n"
    h += '<script src="https://cdn.jsdelivr.net/npm/d3-sankey@0.12.3/dist/d3-sankey.min.js"></script>'
    h += "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12">'
    h += '<div class="card mt-2"><div class="card-body">'
    h += '<h3 class="card-title">Navigation Chart</h3>'
    h += '<p class="card-text">User Navigation Chart for ' + owndomain + ':</p>'
    h += '<div id="navchart-container20250128"><svg id="svgchart20250128" width="600" height="400"></svg></div>'
    h += '<script type="module">' + "\n"
    h += 'const nodes = ' + str(nodes) + ';' + "\n"
    h += 'const links = ' + str(links) + ';' + "\n"
    h += 'const rect = document.getElementById("navchart-container20250128").getBoundingClientRect();'
    h += 'const margin = { top: 1, right: 20, bottom: 5, left: 1 };'
    h += 'const width = Math.round(rect.width) - margin.left - margin.right;'
    h += 'const height = width;'  + "\n"   # make height at least as width

    #  Convert the source and target to internal node indices
    h += 'const LS = d3.map(links, (link) => link.source);'
    h += 'const LT = d3.map(links, (link) => link.target);'
    h += 'const LV = d3.map(links, (link) => link.value);'

    h += 'const N = d3.map(nodes, (node) => node.id);'
    h += 'const G = null;'   # No specific node groups in this case

    #// Create a sankey layout
    h += 'const sankey = d3.sankey()'
    h += '.nodeId(({ index: i }) => N[i])'
    h += '.nodeWidth(10)'
    h += '.nodePadding(10)'
    h += '.nodeAlign(d3.sankeyJustify)'
    h += '.extent(['
    h += '[margin.left, margin.top],'
    h += '[width - margin.right, height - margin.bottom]'
    h += ']);'  + "\n"

    h += 'const { nodes: computedNodes, links: computedLinks } = sankey({'
    h += 'nodes: nodes,'
    h += 'links: links'
    h += '});'  + "\n"

    #// Create the SVG container
    h += 'const svg = d3.select("#svgchart20250128")'
    h += '.attr("width", width)'
    h += '.attr("height", height)'
    h += '.attr("viewBox", [0,0 , width, height])'
    h += '.attr("style", "max-width: 100%; height: auto;  font: 10px sans-serif; height: intrinsic;");'  + "\n"

    # // Add node elements (rectangles)
    h += 'const node = svg'
    h += '.append("g")'
    h += '.attr("stroke", "currentColor")'
    h += '.selectAll("rect")'
    h += '.data(computedNodes)'
    h += '.join("rect")'
    h += '.attr("x", (d) => d.x0)'
    h += '.attr("y", (d) => d.y0)'
    h += '.attr("width", (d) => d.x1 - d.x0)'
    h += '.attr("height", (d) => d.y1 - d.y0)'
    h += '.attr("fill", "#1f77b4");'  + "\n"

    #// Add labels to the nodes
    h += 'svg'
    h += '.append("g")'
    h += '.attr("font-family", "sans-serif")'
    h += '.attr("font-size", 10)'
    h += '.selectAll("text")'
    h += '.data(computedNodes)'
    h += '.join("text")'
    h += '.attr("x", (d) => (d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6))'
    h += '.attr("y", (d) => (d.y1 + d.y0) / 2)'
    h += '.attr("dy", "0.35em")'
    h += '.attr("text-anchor", (d) => (d.x0 < width / 2 ? "start" : "end"))'
    h += '.text((d) => d.id);'  + "\n"

    #// Add link elements (paths)
    h += 'const link = svg'
    h += '.append("g")'
    h += '.attr("fill", "none")'
    h += '.attr("stroke-opacity", 0.5)'
    h += '.selectAll("g")'
    h += '.data(computedLinks)'
    h += '.join("g");'  + "\n"

    h += 'link'
    h += '.append("path")'
    h += '.attr("d", d3.sankeyLinkHorizontal())'
    h += '.attr("stroke", "#ccc")'
    h += '.attr("stroke-width", (d) => Math.max(1, d.width));'  + "\n"

    #// Add titles to the links
    h += 'link'
    h += '.append("title")'
    h += '.text((d) => `${d.source.id} → ${d.target.id}\n${d.value}`);'  + "\n"

    h += '</script>'
    h += '</div></div></div>'
    return h

def is_valid_ip(address):
    try: 
        x = ipaddress.ip_address(address)
        return True
    except:
        return False

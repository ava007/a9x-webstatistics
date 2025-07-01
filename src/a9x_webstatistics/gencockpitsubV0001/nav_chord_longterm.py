# -*- coding: utf-8 -*-
from operator import itemgetter
from .validip import is_valid_ip

# navigation chart in chord-dependency diagram:
# https://observablehq.com/@d3/chord-dependency-diagram/2

def navChordLongterm(d, owndomain, omit):
    data = []

    days = 0
    cnt_ext = 0
    cnt_int = 0
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        # omit days:
        if len(k) > 6:
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
                if cnt_ext > 30:  # top 30 entry domains
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
                if cnt_int > 30:  # consider only top 30 entries for internal traffic
                    break
                    
        days += 1
        if days >= 31:
            break
   
    # d3js horizontal bubble char in case results are available
    h = "\n\n"
    h += '<div class="col-md-12 col-lg-12 col-xxl-12 pt-4">'
    h += '<h3>User Navigation - Long Term</h3>'
    h += '<p>This chart shows the user navigation on ' + owndomain + ':</p>'
    h += '<div id="navchart-lt-container"></div>'
    h += '<script type="module">' + "\n"
    h += 'const data = ' + str(data) + ';' + "\n"
    h += 'const {names, linkValues, categoryFilteredValues, categorySpecificValues, countryToContinent, categoryFilter, categoryPairsMap} = data;'
    h += 'function renderChart(data, options = {}) {'
    h += 'const rect = document.getElementById("navchart-lt-container").getBoundingClientRect();'
    h += 'const margins = { top: 20, right: 20, bottom: 40, left: 20 };'
    h += 'const width = Math.round(rect.width) - margins.left - margins.right;'
    h += 'const height = Math.round(width*0.9);'
    h += 'const innerRadius = Math.min(width, height) * 0.5 - 90;'
    h += 'const outerRadius = innerRadius + 10;' + "\n"

    # Dark mode configuration
    h += "const isDarkMode = () => window?.matchMedia?.('(prefers-color-scheme:dark)')?.matches ?? false;"
    h += 'const backgroundColor = isDarkMode ? "#1a1a1a" : "#ffffff";'
    h += 'const textColor = isDarkMode ? "#ffffff" : "#000000";'
    h += 'const fadedTextColor = isDarkMode ? "#cccccc" : "#666666";' + "\n"

    # Pre-sort data and names for consistent ordering
    h += 'const volumeByName = {};'
    h += 'names.forEach((name, i) => {'
    h += 'volumeByName[name] = d3.sum(data[i]);'
    h += '});' + "\n"

    # Create sorted order: largest first, "Other" last
    h += 'const sortedNames = [...names].sort((a, b) => {'
    h += 'if (a === "Other") return 1;'
    h += 'if (b === "Other") return -1;'
    h += 'return volumeByName[b] - volumeByName[a];'
    h += '});'  + "\n"

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
    h += 'const svg = d3.select("#navchart-lt-container").append("svg")'
    h += '.attr("id","tt20250324")'
    h += '.attr("width", width)'
    h += '.attr("height", height)'
    h += '.attr("viewBox", [-width / 2, -height / 2, width, height])'
    h += '.attr("style", "width: 100%; height: auto; font: 10px sans-serif;");'  + "\n"

    # Add CSS styles for hover effects
    h += 'svg.append("style").text(`'
    h += '.chord-arc { opacity: 1;  }'
    h += '.chord-arc.fade { opacity: 0.2; }'
    h += '.chord-arc:hover { opacity: 0.9; }'
    h += '.chord-ribbon { opacity: 0.8; mix-blend-mode: ${isDarkMode ? "lighten" : "multiply"}; }'
    h += '.chord-ribbon.fade { opacity: 0.1; }'
    h += '.chord-ribbon.filtered { display: none; }'
    h += 'text { fill: ${textColor}; font-weight: bold; }'
    h += '.tick-text { fill: ${fadedTextColor}; font-weight: normal; }'
    h += '`);' + "\n"
    h += 'const chords = chord(matrix);'

    h += 'const group = svg.append("g").selectAll().data(chords.groups).join("g");' + "\n"
    h += 'group.append("path")'
    h += '.attr("class", "chord-arc")'
    h += '.attr("fill", d => colors[d.index])'
    h += '.attr("d", arc)'
    h += '.attr("id", d => `arc-${d.index}`)'
    h += '.on("mouseenter", function(event, d) {'
    # Fade all chords and arcs
    h += 'svg.selectAll(".chord-ribbon, .chord-arc")'
    h += '.classed("fade", true);'
        
    # Build array of connected indices
    h += 'const connectedIndices = new Set();'
        
    # First identify all direct connections through ribbons
    h += 'svg.selectAll(`.chord-ribbon.source-${d.index}, .chord-ribbon.target-${d.index}`)'
    h += '.each(function(ribbonData) {'
    # Only consider visible (not filtered) ribbons
    h += 'if (!d3.select(this).classed("filtered")) {'
    # Only add the connected index (not this arc's index)
    h += 'if (ribbonData.source.index === d.index) {'
    h += 'connectedIndices.add(ribbonData.target.index);'
    h += '} else {'
    h += 'connectedIndices.add(ribbonData.source.index);'
    h += '}'
    h += '}'
    h += '})'
    h += '.classed("fade", false);'
        
    # Add the current arc index
    h += 'connectedIndices.add(d.index);'
        
    # Unfade only directly connected arcs and current arc
    h += 'connectedIndices.forEach(index => {'
    h += 'svg.select(`#arc-${index}`).classed("fade", false);'
    h += '});'
    h += '})'  + "\n"
    h += '.on("mouseleave", function() {'
    # Reset all elements to normal state
    h += 'svg.selectAll(".chord-ribbon, .chord-arc")'
    h += '.classed("fade", false);'
    h += '});' + "\n"

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

    h += 'const ribbons = svg.append("g")'
    h += '.attr("fill-opacity", 0.75)'
    h += '.selectAll()'
    h += '.data(chords)'
    h += '.join("path")'
    h += '.style("mix-blend-mode", "multiply")'
    h += '.attr("fill", d => colors[d.target.index])'
    h += '.attr("d", ribbon);'
    #h += '.append("title")'
    #h += '.text(d => `${names[d.source.index]} → ${names[d.target.index]} ${d.source.value}`);'

    h += 'ribbons.append("title")'
    h += '.text(function(d) {'
    # Get the names of source and target
    h += 'let sourceName = sortedNames[d.source.index];'
    h += 'let targetName = sortedNames[d.target.index];'
      
    # If the ribbon is filtered (hidden), don't show any tooltip
    h += 'if (d3.select(this).classed("filtered")) { return ""; }'
      
    # Create keys for both directions
    h += 'const sourceToTargetKey = `${sourceName}_${targetName}`;'
    h += 'const targetToSourceKey = `${targetName}_${sourceName}`;'
      
    # CHANGED: Handle source-target values based on category filter
    h += 'let sourceToTargetValue, targetToSourceValue;'
    h += 'let lineTitle = "";'
      
    h += 'if (categoryFilter !== "all") {'
    # Try to get category-specific values from categories CSV
    h += 'const sourceOrigKey = `${sourceName}_${targetName}`;'
    h += 'const targetOrigKey = `${targetName}_${sourceName}`;'
        
    h += 'sourceToTargetValue = categorySpecificValues[sourceOrigKey];'
    h += 'targetToSourceValue = categorySpecificValues[targetOrigKey];'
    h += '} else {'
    # Use total values for "All Categories"
    h += 'sourceToTargetValue = categoryFilteredValues[sourceToTargetKey];'
    h += 'targetToSourceValue = categoryFilteredValues[targetToSourceKey];'
    h += '}'
      
    # Build tooltip text
    h += 'if (sourceToTargetValue) {'
    h += 'let fromSourceToTargetValue = formatBigNumber(sourceToTargetValue);'
    h += 'lineTitle += `${fromSourceToTargetValue} ${sourceName} → ${targetName}`;'
    h += '}'
             
    h += 'if (targetToSourceValue && d.source.index !== d.target.index) {'
    h += 'let fromTargetToSourceValue = formatBigNumber(targetToSourceValue);'
    h += 'lineTitle += `\n${fromTargetToSourceValue} ${targetName} → ${sourceName}`;'
    h += '}'
      
    h += 'return lineTitle;'
    h += '});'


    h += 'ribbons.on("mouseenter", function(event, d) {'
    # Fade all chords and arcs
    h += 'svg.selectAll(".chord-ribbon, .chord-arc").classed("fade", true);'
          
    # Keep only this chord visible
    h += 'd3.select(this).classed("fade", false);'
          
    # Keep only connected arcs visible
    h += 'const sourceArc = svg.select(`#arc-${d.source.index}`);'
    h += 'const targetArc = svg.select(`#arc-${d.target.index}`);'
    h += 'sourceArc.classed("fade", false);'
    h += 'targetArc.classed("fade", false);'
    h += '})'
    h += '.on("mouseleave", function() {'
    # Reset all elements to normal state
    h += 'svg.selectAll(".chord-ribbon, .chord-arc").classed("fade", false);'
    h += '});'  + "\n"
    h += '}' + "\n"   # end of function renderChart
    
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

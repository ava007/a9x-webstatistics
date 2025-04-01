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
    if len(sdata) == 0:
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

    h += '
    function prepareData(sdata) {
  const groupedData = d3.rollup(sdata, v => Object.fromEntries(v.map(d => [d.t, d.c])), d => d.d);
  const dates = Array.from(groupedData.keys()).sort();
  const categories = ["desk", "mob", "tab"];
  const transformedData = dates.map(d => {
    let entry = { d };
    let values = groupedData.get(d) || {};
    categories.forEach(c => entry[c] = values[c] ?? 0);
    return entry;
  });
  transformedData.forEach(entry => {
    const sortedCategories = categories.slice().sort((a, b) => entry[b] - entry[a]);
    const sortedEntry = {};
    sortedCategories.forEach(c => sortedEntry[c] = entry[c]);
    Object.assign(entry, sortedEntry);
  });
  return { transformedData, dates, categories };
}

function setupSVG(container) {
  const { width } = container.getBoundingClientRect();
  const height = width * 0.5;
  const margins = { top: 20, right: 20, bottom: 50, left: 40 };
  const svg = d3.select(container).append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height]);
  return { width, height, margins, svg };
}

function drawChart(svg, { width, height, margins }, { transformedData, dates, categories }, vdata, rdata) {
  const stack = d3.stack().keys(categories);
  const series = stack(transformedData);
  const yMax = Math.max(d3.max(series, d => d3.max(d, d => d[1])), d3.max(vdata, d => d.c), d3.max(rdata, d => d.c));

  const x = d3.scaleBand().domain(dates).range([margins.left, width - margins.right]).padding(0.1);
  const y = d3.scaleSymlog().domain([0.1, yMax]).range([height - margins.bottom, margins.top]).nice();
  const color = d3.scaleOrdinal().domain(categories).range(["#42c5f5", "#42f5aa", "#f5a742"]);

  svg.append("g")
    .selectAll("g")
    .data(series)
    .join("g")
    .attr("fill", d => color(d.key))
    .selectAll("rect")
    .data(d => d)
    .join("rect")
    .attr("x", d => x(d.data.d))
    .attr("y", d => y(Math.max(1, isNaN(d[1]) ? 1 : d[1])))
    .attr("height", d => Math.max(0, Math.abs(y(d[0]) - y(d[1]))))
    .attr("width", x.bandwidth());

  const visitline = d3.line().x(d => x(d.d) + x.bandwidth() / 2).y(d => y(d.c));

  svg.append("path")
    .datum(vdata)
    .attr("fill", "none")
    .attr("stroke", "red")
    .attr("stroke-width", 2)
    .attr("d", visitline);

  svg.append("path")
    .datum(rdata)
    .attr("fill", "none")
    .attr("stroke", "lightgrey")
    .attr("stroke-width", 2)
    .attr("d", visitline);

  addPoints(svg, vdata, "red");
  addPoints(svg, rdata, "lightgrey");

  svg.append("g")
    .attr("transform", `translate(0,${height - margins.bottom})`)
    .call(d3.axisBottom(x).tickSizeOuter(0))
    .selectAll("text")
    .attr("transform", "rotate(45)")
    .style("text-anchor", "start");

  svg.append("g")
    .attr("transform", `translate(${margins.left},0)`)
    .call(d3.axisLeft(y).ticks(5));

  addTooltip(svg, x, y);
  addLegend(svg, width, color, categories);
}

function addPoints(svg, data, color) {
  svg.selectAll(`.point-${color}`)
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", d => x(d.d) + x.bandwidth() / 2)
    .attr("cy", d => y(d.c))
    .attr("r", 4)
    .attr("fill", color)
    .attr("stroke", "white")
    .attr("stroke-width", 1);
}

function addTooltip(svg, x, y) {
  const tooltip = d3.select("#mhvchart-container").append("div")
    .style("position", "absolute")
    .style("background", "white")
    .style("padding", "5px")
    .style("border", "1px solid black")
    .style("border-radius", "5px")
    .style("visibility", "hidden")
    .style("pointer-events", "none");

  svg.selectAll("rect")
    .on("mouseover", (event, d) => {
      tooltip.style("visibility", "visible");
    })
    .on("mousemove", (event, d) => {
      tooltip.html(`Date: ${d.data.d}<br>Category: ${d3.select(event.target.parentNode).datum().key}<br>Count: ${d[1] - d[0]}`)
        .style("top", `${event.pageY - 10}px`)
        .style("left", `${event.pageX + 10}px`);
    })
    .on("mouseleave", () => {
      tooltip.style("visibility", "hidden");
    });
}

function addLegend(svg, width, color, categories) {
  const legend = svg.append("g")
    .attr("transform", `translate(${width / 2}, 20)`);

  const legendItem = legend.selectAll(".legend-item")
    .data(categories)
    .enter()
    .append("g")
    .attr("class", "legend-item")
    .attr("transform", (d, i) => `translate(${i * 100},0)`);

  legendItem.append("rect")
    .attr("width", 18)
    .attr("height", 18)
    .attr("fill", d => color(d));

  legendItem.append("text")
    .attr("x", 24)
    .attr("y", 9)
    .attr("dy", "0.35em")
    .text(d => d);
}

const container = document.getElementById("mhvchart-container");
const { transformedData, dates, categories } = prepareData(sdata);
const { svg, width, height, margins } = setupSVG(container);
drawChart(svg, { width, height, margins }, { transformedData, dates, categories }, vdata, rdata);

console.log("Transformed Data:", transformedData);
console.log("Stacked Data:", d3.stack().keys(categories)(transformedData));
    '

    h += "</script>"
    h += '</div>' + "\n"
    return h

# -*- coding: utf-8 -*-
import io, sys, argparse, json, ast
from copy import deepcopy
from datetime import datetime

def genHeader():
    h = '<hmtl>' + "\n"
    h += '<body>' + "\n"
    h += '<div> <canvas id="myChart"></canvas> </div>' + "\n"
    h += '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>' + "\n"
    h += '<script> const ctx = document.getElementById(\'myChart\');' + "\n"
    return h
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--infile", help="filename including path to web server access log that contains input data", default="webstat.json")
  args = parser.parse_args()

  try:
    f = open(args.infile) 
    d = json.load(f) 
  except FileNotFoundError: 
    print("-i file not found")
  except json.JSONDecodeError:
    print("-i json file is not valid")

  lbl = []
  dta = []

  for e in d['days']:
    lbl.append(e)
    dta.append(d['days'][e]['device_hits']['desktop'])


  h = genHeader()
  h += 'new Chart(ctx, {'  + "\n"
  h += ' type: \'bar\',' 
  h += 'data: { ' + "\n" +  'labels: ' + str(lbl) + ',' + "\n"
  h += ' datasets: [{ label: \'User Visits\',  data: ' + str(dta) + ','
  h += '}]' + "\n"
  h += '}, });' + "\n"
  h += '</script></body></html>'

  print(h)

  exit()

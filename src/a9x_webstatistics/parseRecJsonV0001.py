import ast
#import io, sys, argparse, json, ast

def(rec, lasttimerecobj, geoip):
  r = ast.literal_eval(rec)    # parse rec to dict
  dto = datetime.strptime(r['time_local'], "%d/%b/%Y:%H:%M:%S %z")   # 07/Jan/2024:14:06:24 +0000

  # skip already processed data:
  if dto  <=  lasttimerecobj:
     continue
  return

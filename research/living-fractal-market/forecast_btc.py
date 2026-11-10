#!/usr/bin/env python3
"""Runnable BTC hourly research forecaster; Python 3.10+, standard library only."""
import argparse, datetime as dt, json, math, statistics, sys, urllib.parse, urllib.request
API="https://api.binance.com/api/v3/klines"
def candles():
 q=urllib.parse.urlencode({"symbol":"BTCUSDT","interval":"1h","limit":500})
 req=urllib.request.Request(API+"?"+q,headers={"User-Agent":"LivingFractalMarket/0.1"})
 with urllib.request.urlopen(req,timeout=20) as r: raw=json.loads(r.read().decode())
 now=int(dt.datetime.now(dt.timezone.utc).timestamp()*1000)
 rows=[{"t":int(x[0]),"end":int(x[6]),"c":float(x[4])} for x in raw if int(x[6])<now]
 if len(rows)<100: raise ValueError("fewer than 100 closed hourly candles")
 times=[x["t"] for x in rows]
 if times!=sorted(set(times)): raise ValueError("duplicate or unordered candles")
 if any(b-a!=3600000 for a,b in zip(times,times[1:])): raise ValueError("hourly gap detected")
 if any(not math.isfinite(x["c"]) or x["c"]<=0 for x in rows): raise ValueError("invalid close")
 return rows
def build(rows):
 closes=[x["c"] for x in rows]; r=[math.log(b/a) for a,b in zip(closes,closes[1:])]
 recent=r[-72:]; w=[math.exp(-math.log(2)*(len(recent)-1-i)/24) for i in range(len(recent))]
 mu=sum(a*b for a,b in zip(w,recent))/sum(w); sigma=statistics.stdev(r[-168:])
 drift=max(-0.0008,min(0.0008,0.10*mu)); ref=closes[-1]
 issue=dt.datetime.now(dt.timezone.utc).replace(minute=0,second=0,microsecond=0)
 cutoff=dt.datetime.fromtimestamp(rows[-1]["end"]/1000,dt.timezone.utc); forecast=[]
 for h in range(1,25):
  target=issue+dt.timedelta(hours=h); p=ref*math.exp(drift*h); width=sigma*math.sqrt(h)
  forecast.append({"horizon_h":h,"target_utc":target.isoformat().replace("+00:00","Z"),"point_usd":round(p,2),
   "p50_low_usd":round(ref*math.exp(drift*h-.67449*width),2),"p50_high_usd":round(ref*math.exp(drift*h+.67449*width),2),
   "p90_low_usd":round(ref*math.exp(drift*h-1.64485*width),2),"p90_high_usd":round(ref*math.exp(drift*h+1.64485*width),2)})
 return {"schema":"lfm.forecast.v1","asset":"BTC/USDT","venue":"Binance spot","issued_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
  "data_cutoff_utc":cutoff.isoformat(),"reference_price_usd":ref,"model":"LFM-Shrinkage-Drift-0.1","model_status":"experimental; intervals uncalibrated",
  "training_window_candles":len(rows),"hourly_log_return_sigma":sigma,"shrunk_hourly_drift":drift,"forecast":forecast,
  "warnings":["Conservative shrinkage-drift baseline; not a validated alpha model.","Gaussian intervals are uncalibrated until forward evaluation.","BTCUSDT spot is a venue proxy."]}
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); a=p.parse_args()
 try:
  result=build(candles())
  if a.json: print(json.dumps(result,indent=2)); return
  print("{} | {} | reference {:.2f} USD".format(result["model"],result["asset"],result["reference_price_usd"]))
  print("Issued {} | cutoff {}".format(result["issued_at_utc"],result["data_cutoff_utc"]))
  for x in result["forecast"]: print("+{:02d}h {}  {:.2f} USD  (90% approx {:.2f}-{:.2f})".format(x["horizon_h"],x["target_utc"],x["point_usd"],x["p90_low_usd"],x["p90_high_usd"]))
  for x in result["warnings"]: print("WARNING: "+x)
 except Exception as e: print("FORECAST ABSTAINED: {}: {}".format(type(e).__name__,e),file=sys.stderr); sys.exit(2)
if __name__=="__main__": main()

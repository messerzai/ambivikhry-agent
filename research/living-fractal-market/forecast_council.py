#!/usr/bin/env python3
"""Forecast council: independent BTC hourly research baselines, Python 3.10+."""
import argparse, datetime as dt, json, math, statistics, sys, urllib.parse, urllib.request

API = "https://api.binance.com/api/v3/klines"

def get_rows():
    q = urllib.parse.urlencode({"symbol":"BTCUSDT","interval":"1h","limit":500})
    req = urllib.request.Request(API+"?"+q, headers={"User-Agent":"LivingFractalMarket-Council/0.1"})
    with urllib.request.urlopen(req, timeout=20) as r: raw = json.loads(r.read().decode())
    now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp()*1000)
    rows = [{"t":int(x[0]),"end":int(x[6]),"o":float(x[1]),"h":float(x[2]),"l":float(x[3]),"c":float(x[4]),"v":float(x[5])}
            for x in raw if int(x[6]) < now_ms]
    if len(rows)<200: raise ValueError("need 200 closed hourly candles")
    ts=[x["t"] for x in rows]
    if ts != sorted(set(ts)) or any(b-a != 3600000 for a,b in zip(ts,ts[1:])):
        raise ValueError("duplicate, unordered, or missing hourly candles")
    if now_ms-rows[-1]["end"] > 90*60_000: raise ValueError("latest candle stale")
    for x in rows:
        if min(x["o"],x["h"],x["l"],x["c"])<=0 or x["v"]<0 or x["h"]<max(x["o"],x["c"],x["l"]) or x["l"]>min(x["o"],x["c"]):
            raise ValueError("invalid OHLCV candle")
    return rows

def mean(xs): return sum(xs)/len(xs)
def ewma(xs, hl):
    w=[math.exp(-math.log(2)*(len(xs)-1-i)/hl) for i in range(len(xs))]
    return sum(x*y for x,y in zip(xs,w))/sum(w)

def council(rows):
    c=[x["c"] for x in rows]; v=[x["v"] for x in rows]
    r=[math.log(b/a) for a,b in zip(c,c[1:])]
    ref=c[-1]; sig24=statistics.stdev(r[-24:]); sig168=statistics.stdev(r[-168:])
    fast=ewma(r[-24:],8); mid=ewma(r[-72:],24); slow=ewma(r[-168:],56)
    # Independent challengers. All signals are deliberately bounded.
    trend=max(-.0012,min(.0012,(.5*fast+.3*mid+.2*slow)*.25))
    reversion=max(-.00025,min(.00025,math.log(mean(c[-72:])/ref)*.025))
    vol_ratio=sig24/max(sig168,1e-9)
    regime=max(.15,min(.8,.55/max(1,vol_ratio)))
    ensemble=max(-.0012,min(.0012,(.5*fast+.3*mid+.2*slow)*.35*regime))
    # Range/volume pressure proxy: signed candle body weighted by relative volume.
    pressure=[]
    for x in rows[-24:]:
        body=math.log(x["c"]/x["o"])
        rel=min(3.0,x["v"]/(mean(v[-72:]) or 1))
        pressure.append(body*rel)
    flow=max(-.0005,min(.0005,mean(pressure)*.12))
    models={
      "RandomWalk": lambda h: 0.0,
      "TrendOnly": lambda h: trend*math.exp(-(h-1)/16),
      "MeanReversion": lambda h: reversion*(1-math.exp(-h/10)),
      "VolRegimeEnsemble": lambda h: ensemble*math.exp(-(h-1)/10)+reversion*(1-math.exp(-h/12)),
      "VolumePressure": lambda h: flow*math.exp(-(h-1)/5)
    }
    issue=dt.datetime.now(dt.timezone.utc)
    hour=issue.replace(minute=0,second=0,microsecond=0)
    outputs=[]
    for name,step in models.items():
        cumulative=0.0; points=[]
        for h in range(1,25):
            cumulative += step(h)
            # Broad uncalibrated range shared across models; point forecasts remain separate.
            width=max(.0005,min(.03,.65*sig24+.35*sig168))*math.sqrt(h)
            points.append({"h":h,"utc":(hour+dt.timedelta(hours=h)).isoformat().replace("+00:00","Z"),
              "usd":round(ref*math.exp(cumulative),2),
              "p90_low":round(ref*math.exp(cumulative-1.64485*width),2),
              "p90_high":round(ref*math.exp(cumulative+1.64485*width),2)})
        outputs.append({"model":name,"points":points})
    return {"schema":"lfm.council.v1","issued_at_utc":issue.isoformat(),
      "data_cutoff_utc":dt.datetime.fromtimestamp(rows[-1]["end"]/1000,dt.timezone.utc).isoformat(),
      "asset":"BTC/USDT","venue":"Binance spot","reference_price_usdt":ref,
      "diagnostics":{"sigma_24h":sig24,"sigma_168h":sig168,"fast_trend":fast,"medium_trend":mid,"slow_trend":slow,
                     "volatility_ratio":vol_ratio,"bounded_trend_signal":trend,"mean_reversion_signal":reversion,"volume_pressure_signal":flow},
      "models":outputs,
      "warning":"Independent experimental baselines, not validated predictors. Approximate 90% ranges are uncalibrated. Research only."}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); a=p.parse_args()
    try:
        out=council(get_rows())
        if a.json: print(json.dumps(out,indent=2))
        else:
            print(f'Forecast council | BTCUSDT reference {out["reference_price_usdt"]:.2f} | {out["issued_at_utc"]}')
            for m in out["models"]:
                print("\n"+m["model"])
                for x in m["points"]: print(f'+{x["h"]:02d}h {x["utc"]}  {x["usd"]:.2f}  [{x["p90_low"]:.2f}, {x["p90_high"]:.2f}]')
            print(out["warning"])
    except Exception as e:
        print(f"COUNCIL ABSTAINED: {type(e).__name__}: {e}",file=sys.stderr); sys.exit(2)
if __name__=="__main__": main()

from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from .model import ExperimentWeights, Window
from .optimizer import choose_best, report, sweep_angles
from .solar import position

def main():
    p=argparse.ArgumentParser(description="Run a BlindLab v0.1 experiment")
    p.add_argument("--timestamp",default="2026-10-04T12:00:00+00:00")
    p.add_argument("--latitude",type=float,default=6.5244)
    p.add_argument("--longitude",type=float,default=3.3792)
    p.add_argument("--utc-offset",type=float,default=1)
    p.add_argument("--window-azimuth",type=float,default=180)
    p.add_argument("--output",type=Path,default=Path("artifacts/experiment.json"))
    a=p.parse_args()
    dt=datetime.fromisoformat(a.timestamp)
    if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
    sun=position(dt,a.latitude,a.longitude,a.utc_offset)
    window=Window(a.window_azimuth); weights=ExperimentWeights()
    candidates=sweep_angles(window,sun,weights); best=choose_best(candidates)
    payload=report(dt,a.latitude,a.longitude,a.utc_offset,window,sun,weights,candidates,best)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"sun_altitude_deg":round(sun.altitude_deg,3),"sun_azimuth_deg":round(sun.azimuth_deg,3),
                      "best_angle_deg":best.angle_deg,"best_score":round(best.total,6),
                      "artifact":str(a.output)},indent=2))

if __name__=="__main__": main()

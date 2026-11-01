#!/usr/bin/env python3
"""Validate plan.json before publishing. Usage: python3 validate_plan.py [plan.json]"""
import json, sys
p = sys.argv[1] if len(sys.argv) > 1 else "/workspace/wellness/plan/plan.json"
d = json.load(open(p, encoding="utf-8"))
err = []
for k in ("version", "exercises"):
    if k not in d: err.append(f"missing top-level '{k}'")
ids = set()
for i, e in enumerate(d.get("exercises", [])):
    for k in ("id", "nameHe"):
        if not e.get(k): err.append(f"exercise #{i}: missing '{k}'")
    if e.get("id") in ids: err.append(f"duplicate id {e.get('id')}")
    ids.add(e.get("id"))
    if e.get("type", "strength") not in ("strength", "cardio", "timed"): err.append(f"{e.get('id')}: bad type")
    if not isinstance(e.get("sets", 1), int) or e.get("sets", 1) < 1: err.append(f"{e.get('id')}: sets must be int >= 1")
    if e.get("type") in ("cardio", "timed") and not e.get("durationSec"): err.append(f"{e.get('id')}: cardio/timed needs durationSec")
if err: print("INVALID:\n- " + "\n- ".join(err)); sys.exit(1)
print(f"OK: version {d['version']}, {len(d['exercises'])} exercises")

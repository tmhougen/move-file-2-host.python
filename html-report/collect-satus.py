#!/usr/bin/env python3
import sys
import glob
import os
import json

collectedfile="./details.json"
pattern = './**/status.json'

Dict = {}
Dict["applications"] = []
for fname in glob.glob(pattern, recursive=True):
    if os.path.isfile(fname):
        print(fname)
        f = open(fname)
        app = json.load(f)
        Dict["applications"].append(app)
with open(collectedfile, "w") as outfile:
    json.dump(Dict, outfile, indent=2)

sys.exit(0)

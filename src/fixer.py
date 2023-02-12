import json
import os

import config as cfg

files = []
with open('treated-files.json') as f:
    files = json.load(f)

for f in files:
    paths = cfg.SOURCE + [f]
    full_path = os.path.join(*paths)
    # if os.path.exists(full_path):
    #     continue
    # print(f"error with: {full_path}")

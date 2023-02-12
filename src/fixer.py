import json
import os

import config as cfg

files = []
with open('treated-files.json') as f:
    files = json.load(f)

for f in files:
    src, dst = os.path.join(*(cfg.SOURCE + [f])), os.path.join(*(cfg.RENAMES + [f]))

    # if os.path.exists(src):
    #     continue
    # print(f"error with: {src}")

    os.rename(src, dst)

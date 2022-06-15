import sys
import json

import constants.treatment_format as trf

import helpers.util as util

if len(sys.argv) != 2:
    print('enter a filename', file=sys.stderr)
    sys.exit(1)

file_name, = sys.argv[1:]

with open(file_name, 'r') as f:
    data = json.load(f)

keys = (trf.SOURCE_PATH, trf.RENAME_PATH, trf.DESTINATION_PATH)
if not all(key in data for key in keys):
    print("missing treatment format edit key, so can't fix this file")
    sys.exit(2)

paths_dict = {key : data[key] for key in keys}
for key in keys:
    data.pop(key, None)

data[trf.PATHS] = paths_dict

util.write_to_json(data, file_name)

# Overview

Visually confirm whether configuration folders have been correctly made in the user's file system.  
Any number of configurations can be provided to be checked.  
If none are provided, then all configurations in `MVE_CONFIGS` are checked.

# Usage

```
usage: __main__.py [-h] [--dirty] [config_names ...]

positional arguments:
  config_names  name of each config to verify

options:
  -h, --help    show this help message and exit
  --dirty       do not visualise each config's file structure
```

# Example Output

```
loading all configs from $MVE_CONFIGS
verifying the integrity of 1 config
[✓] $MVE_CONFIGS=configs
--- config 1 ---
[✓]   testing/
[✓]     queue/
[✓]     history/
[✓]     errors/
[✓]     + config.json
[✓]     + remaining.json
[ success ] integrity the integrity of config 'testing' has been verified
```

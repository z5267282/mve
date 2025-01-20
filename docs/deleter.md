# Overview

Delete the source folder for a given configuration.  
This will only work once there are:

1. no remaining files;
2. no more treatments in the configuration's `queue` folder.

As stated in the `generator` [documentation](./generator.md) the `mve` project is intended to handle all source videos from editing to deletion.

# Usage

```sh
python3 -m mve log deleter <config>
```

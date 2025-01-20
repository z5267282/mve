# Overview

A series of scripts to edit videos on the command line.  
Configure where videos are stored, view them and enter timestamps of edits.  
Then, edit the videos based off this information.

# Usage

The project can be run in a stateful or stateless mode, depending on whether records should be kept.

```
python3 -m mve <log|no-log> <script> [args...]
```

## 1. Stateful

To edit and record a history of treatments, run the project with these scripts in this order.

| No. | Script                         | Description                                                                 |
| --- | ------------------------------ | --------------------------------------------------------------------------- |
| 1.  | [make](docs/make.md)           | Generate a new configuration in the project history.                        |
| 2.  | [integrity](docs/integrity.md) | Check that configurations have been correctly made in.                      |
| 3.  | [generator](docs/generator.md) | Populate the config's remaining video list.                                 |
| 4.  | [viewer](docs/viewer.md)       | View each remaining video in the config, record treatments and enqueue.     |
| 5.  | [treater](docs/treater.md)     | Perform all treatments on the first enqueued treatment file for the config. |
| 6.  | [deleter](docs/deleter.md)     | Mark the config as complete and delete its source folder.                   |

. Logs are recorded as [sessions](docs/session.md).

## 2. Stateless

For one-off editing where history is not needed, the following scripts can be run.

| Script                   | Description                                              |
| ------------------------ | -------------------------------------------------------- |
| [moment](docs/moment.md) | Make edits for all videos from a particular folder.      |
| [foucs](docs/focus.md)   | Continuously make clips of a particular video.           |
| `combine`                | Join all clips from a folder into a single complication. |

# Configurations Folder

The environment variable `MVE_CONFIGS` should store the full path to the folder storing configurations.  
If it is not set, it will default to the parent folder of the `mve` repository (ie. `..`).

# Overview

View outstanding videos and accordingly prepare a [session](./session.md).  
The video to be edited will be shown to the user and then a command is recorded through a terminal prompt.  
The default video player depending on the operating system will be run.

# Usage

```sh
python3 -m mve log viewer <config>`
```

# Commands

Enter `h` for a full list of commands:

```
[e]nd      | [ start ] [ name ]
    + edit from [ start ] to end of clip.
    + the time is in the form [ integer number of seconds | timestamp in form <[hour]-min-sec> ] 
    + alphanumeric characters, ' ', '.', '-', or '_''

[s]tart    | [ end ] [ name ]
    + edit from start to [ time ] of clip.
    + the time is in the form [ integer number of seconds | timestamp in form <[hour]-min-sec> ] 
    + alphanumeric characters, ' ', '.', '-', or '_''

[m]iddle   | [ start ] [ end ] [ name ]
    + edit from [ start ] to [ end ]
    + start and end are the form [ integer number of seconds | timestamp in form <[hour]-min-sec> ] 
    + alphanumeric characters, ' ', '.', '-', or '_''

[w]hole    | [ name ]
    + edit the entire clip from start to end
    + like running [ s 0 ]
    + alphanumeric characters, ' ', '.', '-', or '_''

[r]ename   | [ name ]
    + rename the clip to [ name ]
    + alphanumeric characters, ' ', '.', '-', or '_''

[d]elete   |
    + delete the clip

[c]ontinue |
    + re-add the current clip so it can be transformed twice

[q]uit     |
    + quit the viewer and save a new treatment structured file to queue/

[h]elp     |
    + print this message
```

.

# Examples

| Command        | Explanaition                                   |
| -------------- | ---------------------------------------------- |
| `m 5 10 hello` | Clip from seconds 5-10 with the name `hello`   |
| `e 1-7 bye`    | Clip from 1m 7s to the end with the name `bye` |

# Reprompt

As it is easy to mistakenly enter a time stamp as a part of a file name, if a file name is entered with any leading numbers then the user is prompted to confirm whether they intended to do so.  
This option can be turned off using the `VERIFY_NAME` option.

For example, here:

```
m 1 2 3
```

the 3 could be mistaken as another timestamp for the `m` command.

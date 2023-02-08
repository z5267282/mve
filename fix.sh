#!/bin/dash

grep -E -o '".*"' src/remaining.json | tr -d '"' | while read vid
do
    grep -F -q "$vid" -r history && continue
    echo "$vid"
done | sed -E -e 's/.*/"&"/' -e '$q' -e 's/$/,/'


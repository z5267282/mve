#!/bin/dash

cd ..
constants="$(grep -E -o '^[A-Z_]* ' error.py | tr -d ' ')"
cd ..
for c in $constants
do
    grep -F -q $c -r helpers *.py || echo $c
done

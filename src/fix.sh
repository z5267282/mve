sed -e '1d' -e '$d' remaining.json | sed -E 's/^ +//' | tr -d '",' | while read vid
do
    grep -F "$vid" -r ../history -q && echo "\"$vid\","
done | sed -E -e 's/^/    /' -e '$s/,$//' -e '1i\
[' -e '$a\
]' > treated-files.json


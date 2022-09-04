#!/bin/sh

for f in $(find 'parsers' -name '*hof_parser.py')
do
    python "$f"
done

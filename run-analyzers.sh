#!/bin/sh

for f in $(find 'analyzers' -name '*.py')
do
    python "$f"
done

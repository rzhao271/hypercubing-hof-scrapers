#!/bin/sh

parsers_dir="parsers"
find "${parsers_dir}" -name '*hof_parser.py' -print0 | xargs -0 python

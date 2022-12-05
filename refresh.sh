#!/bin/sh
./scrape-pages.sh
./run-parsers.sh
./combine-tables.sh
./run-analyzers.sh

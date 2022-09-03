# Hypercubing HoF Scrapers

These scripts download various official hypercubing hall of fame pages
and parse out the data into CSV files of the form

```
puzzle-name, solve-number, solver-name, solve-date-as-epoch-timestamp
```

`puzzle-name` and `solver-name` can have spaces in them. 
`solve-number` is specific to a puzzle.
The output CSV files are in UTF-8 and sometimes contain 
non-ASCII characters for the `solver-name` field.

## What's a hypercubing hall of fame page?

"Hypercubing" is a hobby where one solves higher-dimensional 
twisty puzzles. The most popular example is the [four-dimensional
3x3x3x3](https://superliminal.com/cube/cube.htm).
"Twisty puzzle" is a more generic term for "Rubik's cube".
There are currently a few programs one can use for hypercubing,
and some of the puzzles have official hall of fame (HoF) pages set up.
To be placed on an official HoF page, after one solves the puzzle,
they must e-mail the page owner with their log file.

The most popular hypercubing HoF is the 
[MagicCube4D (MC4D) HoF](https://superliminal.com/cube/halloffame.htm).

## Repository prerequisites

1. Something to run `.sh` files.
2. Python with virtualenv.

## Instructions to generate the CSVs

1. Set up a virtualenv for the repository and load in the requirements 
with `python -m pip install -r requirements.txt`.
2. Run `./scrape-pages.sh` to download the hall of fame pages to `pages/`.
3. Run `python parsers/<parser-file.py>` to parse an individual 
hall of fame page and generate a CSV in `tables/`.
4. Run `./combine-tables.sh` to combine all the generated HoF CSVs.
This step creates the file `tables/combined.csv`.

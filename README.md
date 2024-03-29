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

## Instructions to generate the tables and figures

1. Set up a virtualenv for the repository and load in the requirements 
with `python -m pip install -r requirements.txt`.
2. Run `./scrape-pages.sh` to download the hall of fame pages to `pages/`.
3. Run `./run-parsers.sh` to parse the pages and generate CSVs in `tables/`.
4. Run `./combine-tables.sh` to combine all the generated HoF CSVs into
`tables/combined.csv`.
5. Run `./run-analyzers.sh` to run the various analyzers in `analyzers/`.
The analyzers create CSVs in `tables/` and PNGs in `figures/`.

## Sample generated data

`tables/m120c-hof.csv`
```csv
Magic 120-cell,1,Noel Chalmers,1229155200.0
Magic 120-cell,2,Matt Galla,1293782400.0
Magic 120-cell,3,Adam Ford,1299571200.0
Magic 120-cell,4,Nan Ma,1308466800.0
Magic 120-cell,5,Kitti Varga,1313910000.0
Magic 120-cell,6,Andrey Astrelin,1314860400.0
Magic 120-cell,7,Philip Strimpel,1353484800.0
Magic 120-cell,8,Raymond Zhao,1409382000.0
Magic 120-cell,9,Alvin Yang,1437375600.0
Magic 120-cell,10,Guderian Raborg,1451030400.0
Magic 120-cell,11,Douglas Shamlin,1470553200.0
Magic 120-cell,12,Jeremy Shahan,1491462000.0
Magic 120-cell,13,Michiel Vandecappelle,1611734400.0
Magic 120-cell,14,Charles Doan,1620975600.0
Magic 120-cell,15,Djair Maynart,1639123200.0
```

`tables/recent_solvers.csv`
```csv
solver,puzzle_name,solve_num
Robin Essenburg,Physical 2^4,34
Robin Essenburg,5^4,80
余朗坤,5^4,79
Kevin Liu,3^6,17
Robin Essenburg,4^4,105
Adrián Vasvári,Physical 2^4,33
Robin Essenburg,3^4,488
Langkun Yu (余朗坤),3^5,88
George Jeno,Physical 2^4,32
Nicole Sheehan,Physical 2^4,31
```

## Known issues

The largest issue is that some names appear different on different halls of
fame. The data should be interpreted as an approximation rather than as
exact figures.

## References

- [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

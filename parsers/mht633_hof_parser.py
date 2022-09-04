from os import path

from bs4 import BeautifulSoup
from dateutil import parser

from parser_utils import process_name, write_csv

# In-file: pages/mht633-hof.html
# Out-file: tables/mht633-hof.csv

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../pages/mht633-hof.html')
out_file = path.join(script_dir, '../tables/mht633-hof.csv')

with open(in_file) as f:
    soup = BeautifulSoup(f, 'html.parser')

# Each entry holds { puzzle, solve_count, solver_name, solve_date }
entries = []

def parse_date(s):
    parsed_date = parser.parse(s, dayfirst=False)
    return parsed_date.timestamp()

def parse_puzzle_section(puzzle_name, table):
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        solve_count = tds[0].div.string
        solver_name = process_name(tds[1])
        solve_date = parse_date(tds[2].div.string)
        entries.append({
            'puzzle': puzzle_name,
            'solve_count': solve_count,
            'solver_name': solver_name,
            'solve_date': solve_date
        })

tables = soup.find_all('table')
assert len(tables) == 7

for table in tables:
    puzzle_name = ('MHT633 ' +
                   table.previous_sibling.previous_sibling.string)
    parse_puzzle_section(puzzle_name, table)

write_csv(out_file, entries)

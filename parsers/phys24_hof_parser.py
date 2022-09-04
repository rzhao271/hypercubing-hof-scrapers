from os import path

from bs4 import BeautifulSoup
from dateutil import parser

from parser_utils import process_name, write_csv

# In-file: pages/phys24-hof.html
# Out-file: tables/phys24-hof.csv

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../pages/phys24-hof.html')
out_file = path.join(script_dir, '../tables/phys24-hof.csv')

with open(in_file) as f:
    # The file has a bad tag
    soup = BeautifulSoup(f, 'html5lib')

# Each entry holds { puzzle, solve_count, solver_name, solve_date }
entries = []

def parse_date(s):
    parsed_date = parser.parse(s, dayfirst=False)
    return parsed_date.timestamp()

def parse_puzzle_section(puzzle_name, table):
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        # One of the tr tags is an opening tag
        # when it should be a closing tag
        if not len(tds):
            continue
        solve_count = tds[0].div.string
        solver_name = process_name(tds[1])
        # Special case for A. Farkas
        if solver_name == 'Andy Farkas':
            solver_name = 'A. Farkas'
        solve_date = parse_date(tds[2].div.string)
        entries.append({
            'puzzle': puzzle_name,
            'solve_count': solve_count,
            'solver_name': solver_name,
            'solve_date': solve_date
        })

table = soup.table
parse_puzzle_section('Physical 2^4', table)
write_csv(out_file, entries)

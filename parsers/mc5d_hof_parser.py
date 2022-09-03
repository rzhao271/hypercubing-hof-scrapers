from os import path

from bs4 import BeautifulSoup
from dateutil import parser

from parser_utils import process_name, write_csv

# In-file: pages/mc5d-hof.html
# Out-file: tables/mc5d-hof.csv

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../pages/mc5d-hof.html')
out_file = path.join(script_dir, '../tables/mc5d-hof.csv')

with open(in_file) as f:
    soup = BeautifulSoup(f, 'html.parser')

# Each entry holds { puzzle, solve_count, solver_name, solve_date }
entries = []

def parse_date(td):
    if td.strings:
        s = ''.join(td.strings)
        # Take out using MC7D clarifications
        if ' (' in s:
            s = s[:s.index(' (')]
    else:
        s = td.string
    # Special case for Matthew Sheerin's 7^5 solve
    if 'Friday the 13th,' in s and 'Nov 2009' in s:
        s = '11/13/09'
    parsed_date = parser.parse(s, dayfirst=False, yearfirst=False)    
    return parsed_date.timestamp()

def parse_puzzle_section(puzzle_name, table):
    for i, tr in enumerate(table.find_all('tr')):
        tds = tr.find_all('td')
        solve_count = i + 1
        solver_name = process_name(tds[0])
        solve_date = parse_date(tds[1])
        entries.append({
            'puzzle': puzzle_name,
            'solve_count': solve_count,
            'solver_name': solver_name,
            'solve_date': solve_date
        })

tables = soup.find_all('table')[1:-3]
assert len(tables) == 6

for i in range(6):
    parse_puzzle_section(f'{i + 2}^5', tables[i])

write_csv(out_file, entries)

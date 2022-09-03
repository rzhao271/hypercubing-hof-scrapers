from os import path

from bs4 import BeautifulSoup
from dateutil import parser

# In-file: pages/mht633-hof.html
# Out-file: tables/mht633-hof.csv

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../pages/mht633-hof.html')
out_file = path.join(script_dir, '../tables/mht633-hof.csv')

with open(in_file) as f:
    soup = BeautifulSoup(f, 'html.parser')

# Each entry holds { puzzle, solve_count, solver_name, solve_date }
entries = []

def process_name(td):
    def omit_age(s):
        # exclude " at age <age>"
        unwanted_matches = [' at age']
        for unwanted_match in unwanted_matches:
            if unwanted_match in s:
                s = s[:s.index(unwanted_match)]
        return s
    fragments = []
    for s in td.strings:
        fragments.append(s)
    joined_strings = ' '.join(fragments)
    omit_age_string = omit_age(joined_strings).strip()
    return omit_age_string

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
    puzzle_name = table.previous_sibling.previous_sibling.string
    parse_puzzle_section(puzzle_name, table)

# { puzzle, solve_count, solver_name, solve_date }
with open(out_file, 'w') as f:
    for entry in entries:
        f.write(f'{entry["puzzle"]}, {entry["solve_count"]}, ' + 
                f'{entry["solver_name"]}, {entry["solve_date"]}\n')

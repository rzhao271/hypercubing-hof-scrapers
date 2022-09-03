from os import path

from bs4 import BeautifulSoup
from dateutil import parser

# In-file: pages/mc4d-hof.html
# Out-file: tables/mc4d-hof.csv

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../pages/mc4d-hof.html')
out_file = path.join(script_dir, '../tables/mc4d-hof.csv')

with open(in_file) as f:
    soup = BeautifulSoup(f, 'html.parser')

# Each entry holds { puzzle, solve_count, solver_name, solve_date }
entries = []

def process_name(td):
    def omit_age(s):
        # exclude ", @<age>" and " at <age>"
        unwanted_matches = [', @', ', at age', ' at age', ' on ']
        for unwanted_match in unwanted_matches:
            if unwanted_match in s:
                s = s[:s.index(unwanted_match)]
        return s
    joined_strings = ''.join(td.strings).strip()
    omit_age_string = omit_age(joined_strings)
    return omit_age_string

def parse_date(s):
    if s.startswith('~'):
        s = s[1:]
    parsed_date = parser.parse(s, dayfirst=False)    
    return parsed_date.timestamp()

def parse_puzzle_section(puzzle_name, table):
    for tr in table.tbody.find_all('tr'):
        tds = tr.find_all('td')
        solve_count = tds[0].div.string.strip()
        solver_name = process_name(tds[1])
        solve_date = parse_date(tds[2].div.string.strip())
        entries.append({
            'puzzle': puzzle_name,
            'solve_count': solve_count,
            'solver_name': solver_name,
            'solve_date': solve_date
        })

tables = [table for table in soup.find_all('table') if
    str(table.caption).startswith('<caption>Full')]
assert len(tables) == 3

parse_puzzle_section('3^4', tables[0])
parse_puzzle_section('4^4', tables[1])
parse_puzzle_section('5^4', tables[2])

# { puzzle, solve_count, solver_name, solve_date }
with open(out_file, 'w') as f:
    for entry in entries:
        f.write(f'{entry["puzzle"]}, {entry["solve_count"]}, ' + 
                f'{entry["solver_name"]}, {entry["solve_date"]}\n')

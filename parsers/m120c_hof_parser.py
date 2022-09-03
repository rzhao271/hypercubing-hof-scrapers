from os import path

from bs4 import BeautifulSoup
from dateutil import parser

from writer import write_csv

# In-file: pages/m120c-hof.html
# Out-file: tables/m120c-hof.csv

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../pages/m120c-hof.html')
out_file = path.join(script_dir, '../tables/m120c-hof.csv')

with open(in_file) as f:
    soup = BeautifulSoup(f, 'html.parser')

# Each entry holds { puzzle, solve_count, solver_name, solve_date }
entries = []

def process_name(td):
    def omit_age(s):
        # exclude strings like "@<age>"
        unwanted_matches = ['@age', ' using', ' (']
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
    parsed_date = parser.parse(s, dayfirst=False, yearfirst=False)
    return parsed_date.timestamp()

def parse_puzzle_section(puzzle_name, table):
    for i, tr in enumerate(table.find_all('tr')):
        tds = tr.find_all('td')
        solve_count = i + 1
        solver_name = process_name(tds[0])
        solve_date = parse_date(tds[1].string)
        entries.append({
            'puzzle': puzzle_name,
            'solve_count': solve_count,
            'solver_name': solver_name,
            'solve_date': solve_date
        })

# This is what happens when your page uses tables to hold data
# and do layout at the same time.
table = soup.table.find('table', id='AutoNumber5').table
parse_puzzle_section('Magic 120-cell', table)
write_csv(out_file, entries)

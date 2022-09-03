from os import path

from bs4 import BeautifulSoup
from dateutil import parser

from writer import write_csv

# In-file: pages/mc7d-hof.html
# Out-file: tables/mc7d-hof.csv

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../pages/mc7d-hof.html')
out_file = path.join(script_dir, '../tables/mc7d-hof.csv')

with open(in_file) as f:
    # The MC7D page has some incorrect tr tags
    soup = BeautifulSoup(f, 'html5lib')

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
    fragments = []
    for s in td.strings:
        fragments.append(s)
    joined_strings = ' '.join(fragments) 
    omit_age_string = omit_age(joined_strings)
    return omit_age_string

def parse_date(s):
    parsed_date = parser.parse(s, dayfirst=False)
    return parsed_date.timestamp()

def parse_puzzle_section(puzzle_name, table):
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        solve_count = tds[0].div.string
        solver_name = process_name(tds[1])
        solve_date = parse_date(tds[2].div.a.string)
        entries.append({
            'puzzle': puzzle_name,
            'solve_count': solve_count,
            'solver_name': solver_name,
            'solve_date': solve_date
        })

tables = soup.find_all('table')

for dim in range(2):
    for size in range(3):
        if dim * 3 + size == len(tables):
            break
        parse_puzzle_section(f'{size + 3}^{dim + 6}', tables[dim * 3 + size])

write_csv(out_file, entries)

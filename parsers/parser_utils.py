import re

def write_csv(out_file, entries):
    with open(out_file, 'w') as f:
        for entry in entries:
            f.write(f'{entry["puzzle"]},{entry["solve_count"]},' +
                    f'{entry["solver_name"]},{entry["solve_date"]}\n')

regex = '(,? at age |,? ?@|\(video| on | using |\(?aka ).*$'
unwanted_matches = re.compile(regex, flags=re.IGNORECASE)
def process_name(td):
    fragments = []
    for s in td.strings:
        fragments.extend([fragment.strip(',') for fragment in s.split()])
    fragments = [fragment for fragment in fragments if len(fragment)]
    joined_string = ' '.join(fragments)
    filtered_string = unwanted_matches.sub('', joined_string).strip()
    return filtered_string

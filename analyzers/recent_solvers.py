from os import path

import pandas as pd

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../tables/combined.csv')
out_file = path.join(script_dir, '../tables/recent_solvers.csv')

headers = ['puzzle_name', 'solve_num', 'solver', 'solve_epoch']
df = pd.read_csv(in_file, names=headers)

# Get 10 most recent solvers
df = df.sort_values(by='solve_epoch', ascending=False).head(10)
df = df[['solver', 'puzzle_name', 'solve_num']]
df.to_csv(out_file, index=False)

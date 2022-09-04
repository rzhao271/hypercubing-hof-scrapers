from math import ceil
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../tables/combined.csv')
solve_order_rates_file = path.join(script_dir,
    '../tables/solve_order_rates.csv')
solve_order_durations_plot_file = path.join(script_dir,
    '../figures/solve_order_durations.png')

def process_duration(d):
    # Convert seconds to years
    return d / (60 * 60 * 24 * 365.25)

headers = ['puzzle_name', 'solve_num', 'solver', 'solve_epoch']
df = pd.read_csv(in_file, names=headers)

# Group df by solver
groups = df.groupby(by='solver')

# Get solve durations
solve_duration_headers = ['solver', 'puzzles_solved',
    'total_duration_years', 'years_per_solve']
solve_duration_records = []
for solver, group in groups:
    group = group.sort_values(by='solve_epoch')
    puzzles_solved = len(group)
    epoch_list = group['solve_epoch'].tolist()
    total_duration_years = process_duration(
        float(epoch_list[-1]) - float(epoch_list[0]))
    years_per_solve = total_duration_years / puzzles_solved
    solve_duration_records.append((solver, puzzles_solved,
        total_duration_years, years_per_solve))

solve_duration_df = pd.DataFrame.from_records(solve_duration_records,
    columns=solve_duration_headers)
solve_duration_df = (solve_duration_df
    .loc[solve_duration_df['puzzles_solved'] > 1]
    .sort_values(by=['years_per_solve', 'puzzles_solved'],
                 ascending=[True, False]))

# Include the header this time for clarity
# Save to a CSV
solve_duration_df.to_csv(solve_order_rates_file, index=False)
max_duration = ceil(solve_duration_df['total_duration_years'].max())
solve_order_durations = solve_duration_df['total_duration_years'].tolist()

# Create a histogram for solve order durations
fig, ax = plt.subplots(figsize=(12, 10))
ax.hist(solve_order_durations, bins=np.arange(max_duration + 1))
ax.set_xlabel('Solve order duration (years)', fontsize=16)
ax.set_ylabel('Number of non-singular solve orders of that duration',
    fontsize=16)
ax.set_title('Non-singular solve order durations', fontsize=20)
ax.set_xticks(np.arange(max_duration + 1))
fig.tight_layout()
fig.savefig(solve_order_durations_plot_file)
plt.close(fig)

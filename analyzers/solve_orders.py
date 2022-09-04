from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../tables/combined.csv')
solve_order_by_solver_file = path.join(script_dir,
    '../tables/solve_order_by_solver.csv')
solve_order_by_solver_uncommon_file = path.join(script_dir,
    '../tables/solve_order_by_solver_uncommon.csv')
solve_order_frequencies_file = path.join(script_dir,
    '../tables/solve_order_frequencies.csv')
solve_order_frequencies_plot_file = path.join(script_dir,
    '../figures/top_solve_orders.png')
solve_order_durations_plot_file = path.join(script_dir,
    '../figures/solve_order_durations.png')

headers = ['puzzle_name', 'solve_num', 'solver', 'solve_epoch']
df = pd.read_csv(in_file, names=headers)

# Group df by solver
groups = df.groupby(by='solver')

# We first want solve orders by solver
solve_order_by_solver_headers = ['solver', 'solve_order', 'total_duration']
solve_order_by_solver_records = []
for solver, group in groups:
    group = group.sort_values(by='solve_epoch')
    solve_order = '->'.join(group['puzzle_name'].tolist())
    epoch_list = group['solve_epoch'].tolist()
    total_duration = float(epoch_list[-1]) - float(epoch_list[0])
    solve_order_by_solver_records.append((solver, solve_order, total_duration))

solve_order_df = pd.DataFrame.from_records(solve_order_by_solver_records,
    columns=solve_order_by_solver_headers)

# Include the header this time for clarity
# Save to a CSV
solve_order_df.to_csv(solve_order_by_solver_file, index=False)

# By uncommon we mean that we want to see solve orders
# where the solver never solved the 3^4, but we also kick out
# solvers who only solved the physical 2^4 or only the 3^5
solve_order_df_uncommon = solve_order_df.loc[
    (~solve_order_df['solve_order'].str.contains('3\^4'))
    & (~solve_order_df['solve_order'].str.fullmatch('Physical 2\^4'))
    & (~solve_order_df['solve_order'].str.fullmatch('3\^5'))]
solve_order_df_uncommon.to_csv(solve_order_by_solver_uncommon_file, index=False)

solve_order_frequencies_df = solve_order_df
solve_order_frequencies_df['count'] = (solve_order_frequencies_df
    .groupby(by='solve_order')['solve_order']
    .transform('count'))
solve_order_frequencies_df = (solve_order_frequencies_df
    [['solve_order', 'count']]
    .drop_duplicates()
    .sort_values(by=['count', 'solve_order'], ascending=[False, True]))

# Save to another CSV
solve_order_frequencies_df.to_csv(solve_order_frequencies_file,
    columns=['solve_order', 'count'], index=False)

# Reverse the data for the bar chart
solve_order_frequencies_df = (solve_order_frequencies_df
    .loc[solve_order_frequencies_df['count'] > 1].loc[::-1])
solve_orders = solve_order_frequencies_df['solve_order'].tolist()
counts = solve_order_frequencies_df['count'].tolist()

# Create a bar chart
fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.barh(solve_orders, counts)
ax.bar_label(bars, padding=3)
ax.set_xlabel('Number of solvers', fontsize=16)
ax.set_ylabel('Solve order', fontsize=16)
ax.set_title('Most frequent solve orders', fontsize=20)
fig.tight_layout()
fig.savefig(solve_order_frequencies_plot_file)

def process_duration(d):
    # Convert seconds to years
    return d / (60 * 60 * 24 * 365.25)

solve_order_durations = [process_duration(d) for d in
    solve_order_df['total_duration'].tolist() if d > 0]

# Create a histogram for solve order durations
ax.clear()
ax.hist(solve_order_durations, bins=np.arange(21))
ax.set_xlabel('Solve order duration (years)', fontsize=16)
ax.set_ylabel('Number of non-singular solve orders of that duration',
    fontsize=16)
ax.set_title('Non-singular solve order durations', fontsize=20)
ax.set_xticks(np.arange(21))
fig.tight_layout()
fig.savefig(solve_order_durations_plot_file)

plt.close(fig)

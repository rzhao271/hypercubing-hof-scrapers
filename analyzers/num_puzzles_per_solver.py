from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../tables/combined.csv')
out_figure_file = path.join(script_dir, '../figures/num_puzzles_per_solver.png')
out_table_file = path.join(script_dir, '../tables/num_puzzles_per_solver.csv')

headers = ['puzzle_name', 'solve_num', 'solver', 'solve_epoch']
df = pd.read_csv(in_file, names=headers)

# Get number of puzzles solved per solver
df['num_solved'] = (df.groupby(by='solver', sort=False)['solver']
    .transform('count'))

counts_by_solver = (df[['solver', 'num_solved']]
    .sort_values(by='num_solved', ascending=False).drop_duplicates())
counts_by_solver.to_csv(out_table_file, header=False, index=False)

# Now get number of solvers that have solved x puzzles for x = 1, 2, 3, etc.
per_solve_counts = (counts_by_solver.groupby(by='num_solved')['num_solved']
    .count())

x = per_solve_counts.index.tolist()
y = per_solve_counts.tolist()
mean = np.sum(np.prod([x, y], axis=0)) / np.sum(y)
print(f'For reference, the mean number of puzzles solved '
      f'per solver is {mean:.2f}.')

# Create a bar chart
fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.bar(x, y)
ax.bar_label(bars, padding=3)
ax.set_xlabel('Number of puzzles solved (N)', fontsize=16)
ax.set_ylabel('Number of solvers who have solved N puzzles', fontsize=16)
ax.set_title('Number of puzzles solved per solver', fontsize=20)
ax.set_xticks(np.arange(1, per_solve_counts.index.max() + 1))
fig.tight_layout()
fig.savefig(out_figure_file)
plt.close(fig)

from os import path

import matplotlib.pyplot as plt
import pandas as pd

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../tables/combined.csv')
out_file = path.join(script_dir, '../figures/num_solvers.png')

headers = ['puzzle_name', 'solve_num', 'solver', 'solve_epoch']
df = pd.read_csv(in_file, names=headers)

# Group df by puzzle and do a count
groups = df.groupby(by='puzzle_name')

bar_data = []
for name, group in groups:
   bar_data.append((name, len(group)))
# Sort by number of solvers decreasing,
# then by puzzle name increasing
bar_data.sort(key=lambda x: (x[1], -ord(x[0][0])))

# Create a bar-chart
fig, ax = plt.subplots(figsize=(12, 10))
names, counts = zip(*bar_data)
bars = ax.barh(names, counts)
ax.bar_label(bars, padding=3)
ax.set_xlabel('Number of solvers', fontsize=16)
ax.set_ylabel('Puzzle', fontsize=16)
ax.set_title('Number of solvers per puzzle', fontsize=20)
fig.tight_layout()
fig.savefig(out_file)
plt.close(fig)

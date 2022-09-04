import datetime
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../tables/combined.csv')
out_file = path.join(script_dir, '../figures/solution_month.png')

headers = ['puzzle_name', 'solve_num', 'solver', 'solve_epoch']
df = pd.read_csv(in_file, names=headers)

def get_month(ts):
    parsed_date = datetime.datetime.fromtimestamp(float(ts))
    return parsed_date.month

months = [get_month(ts) for ts in df['solve_epoch']]
months_df = pd.DataFrame(months, columns=['month'])
months_df['num_solutions'] = (months_df.groupby(by='month')['month']
    .transform('count'))
months_df = months_df.drop_duplicates().sort_values(by='month')

# Create a bar chart
fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.bar(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
              months_df['num_solutions'].tolist())
ax.bar_label(bars, padding=3)
ax.set_xlabel('Month', fontsize=16)
ax.set_ylabel('Count', fontsize=16)
ax.set_title('Month of HoF solution dates', fontsize=20)
fig.tight_layout()
fig.savefig(out_file)
plt.close(fig)

import datetime
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../tables/combined.csv')
out_file = path.join(script_dir, '../figures/solution_month_sandbox.png')

headers = ['puzzle_name', 'solve_num', 'solver', 'solve_epoch']
df = pd.read_csv(in_file, names=headers)

# The puzzle to focus on
df = df.loc[df['puzzle_name'] == '5^4']

def get_month(ts):
    parsed_date = datetime.datetime.fromtimestamp(float(ts))
    return parsed_date.month

months = [get_month(ts) for ts in df['solve_epoch']]
months_df = pd.DataFrame(months, columns=['month'])
months_df['num_solutions'] = (months_df.groupby(by='month')['month']
    .transform('count'))
months_df = months_df.drop_duplicates()

# Some months could have no solves so we can't just call tolist
months_df = months_df.set_index('month')
months_dict = months_df.to_dict()['num_solutions']
month_solve_data = [months_dict.get(i, 0) for i in range(12)]

# Create a bar chart
fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.bar(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
              month_solve_data)
ax.bar_label(bars, padding=3)
ax.set_xlabel('Month', fontsize=16)
ax.set_ylabel('Count', fontsize=16)
ax.set_title('Month of HoF solution dates', fontsize=20)
fig.tight_layout()
fig.savefig(out_file)
plt.close(fig)

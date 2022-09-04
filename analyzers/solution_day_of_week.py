import datetime
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../tables/combined.csv')
out_file = path.join(script_dir, '../figures/solution_day_of_week.png')

headers = ['puzzle_name', 'solve_num', 'solver', 'solve_epoch']
df = pd.read_csv(in_file, names=headers)

def get_day_of_week(ts):
    parsed_date = datetime.datetime.fromtimestamp(float(ts))
    return parsed_date.weekday()

weekdays = [get_day_of_week(ts) for ts in df['solve_epoch']]
weekdays_df = pd.DataFrame(weekdays, columns=['weekday'])
weekdays_df['num_solutions'] = (weekdays_df.groupby(by='weekday')['weekday']
    .transform('count'))
weekdays_df = weekdays_df.drop_duplicates().sort_values(by='weekday')

# Create a bar chart
fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.bar(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
              weekdays_df['num_solutions'].tolist())
ax.bar_label(bars, padding=3)
ax.set_xlabel('Day of week', fontsize=16)
ax.set_ylabel('Count', fontsize=16)
ax.set_title('Day of week of HoF postings', fontsize=20)
fig.tight_layout()
fig.savefig(out_file)
plt.close(fig)

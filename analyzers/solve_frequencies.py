import datetime
from os import path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas as pd

script_dir = path.dirname(path.realpath(__file__))
in_file = path.join(script_dir, '../tables/combined.csv')
events_out_file = path.join(script_dir, '../figures/solve_frequencies_events.png')
violin_out_file = path.join(script_dir, '../figures/solve_frequencies_violin.png')

headers = ['puzzle_name', 'solve_num', 'solver', 'solve_epoch']
df = pd.read_csv(in_file, names=headers)

# Group df by puzzle
groups = df.groupby(by='puzzle_name')

def format_date(date):
    parsed_date = datetime.datetime.fromtimestamp(float(date))

    # Get next year and this year
    parsed_date_next_year_begin = datetime.datetime(
        parsed_date.year + 1, 1, 1)
    parsed_date_year_begin = datetime.datetime(
        parsed_date.year, 1, 1)

    # Calculate the residue
    delta_current_year = parsed_date - parsed_date_year_begin
    delta_year = parsed_date_next_year_begin - parsed_date_year_begin
    residue = delta_current_year.total_seconds() / delta_year.total_seconds()
    
    # Example: we get the number 1988.1 for a solve 1/10th of the year
    return parsed_date.year + residue

def format_dates(dates):
    return [format_date(date) for date in dates]

data = []
for name, group in groups:
   data.append((name, len(group), 
                format_dates(group['solve_epoch'].tolist())))

# Sort by number of solvers decreasing,
# then by puzzle name increasing
data.sort(key=lambda x: (x[1], -ord(x[0][0])))

# Create a violin plot
fig, ax = plt.subplots(figsize=(12, 10))
labels, _, events = zip(*data)

def setup_axes(fig, ax):
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylabel('Puzzle', fontsize=16)
    ax.set_yticks(np.arange(len(labels)), labels=labels)
    ax.set_xticks(np.arange(1985, 2024))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.grid(axis='x')
    ax.set_title('Frequency of various puzzle solves', fontsize=20)
    fig.tight_layout()
   
ax.violinplot(events, positions=np.arange(len(labels)), 
              vert=False, showmedians=True)
setup_axes(fig, ax)
fig.savefig(violin_out_file)

# The event bars are more intense so we can keep the violin plot
# for reference
ax.clear()
ax.violinplot(events, positions=np.arange(len(labels)), 
              vert=False, showextrema=False)
ax.eventplot(events)
setup_axes(fig, ax)
fig.savefig(events_out_file)
plt.close(fig)

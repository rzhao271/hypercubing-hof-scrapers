def write_csv(out_file, entries):
    with open(out_file, 'w') as f:
        for entry in entries:
            f.write(f'{entry["puzzle"]},{entry["solve_count"]},' +
                    f'{entry["solver_name"]},{entry["solve_date"]}\n')

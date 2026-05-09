#!/usr/bin/env python3

# File: run_query_w_date.py

"""
requires a parameter; the name of a file containing
a valid sql query with {today} place holders.
"""

# When running from RBC:
# helpers found in code
# sql_code is code.sql 

import sys
try:
    from src import helpers
except ImportError: # running from RBC
    from code import helpers
try:
    from src import sql_code
except ImportError:
    from code import sql as sql_code

today = helpers.eightdigitdate
six_mo_ago = helpers.six_months_ago
query_file = sys.argv[1]
parts = query_file.split(".")
parts = parts[0].split("_")
part = parts[-1]
#_ = input(f"{part=}")
if part == "f6": day = helpers.six_months_ago
elif part == "f": day = helpers.eightdigitdate
with open(query_file, 'r') as stream:
    query = stream.read().format(day=day)
#_ = input(query)
#print(day)
outfile = "query_output.csv"
yn = input(f"Send data to {outfile}? (y/n): ")
if yn and yn[0] in 'yY':
    sql_code.query2csv(query, outfile)
else:
    print(sql_code.query_keys(query))
    res = sql_code.fetch(query, from_file=False)
    for line in res:
        print(line)



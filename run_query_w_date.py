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

query_file = sys.argv[1]
with open(sys.argv[1], 'r') as stream:
    query = stream.read().format(today=today)
#_ = input(query)
#print(today)
outfile = "query_output.csv"
yn = input(f"Send data to {outfile}? (y/n): ")
if yn and yn[0] in 'yY':
    sql_code.query2csv(query, outfile)
else:
    res = sql_code.fetch(query, from_file=False)
    for line in res:
        print(res)



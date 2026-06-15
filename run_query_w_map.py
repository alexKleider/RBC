#!/usr/bin/env python3

# File: run_query_w_map.py

"""
<file> (required param): the name of a file
containing a valid sql query, possibly with
{named} place holders in which case <mapping>
must be provided to supply corresponding values.
"""


# When running from RBC:
# helpers found in code
# sql_code is code.sql 

import sys
import json
try:
    from src import helpers
except ImportError: # running from RBC
    from code import helpers
try:
    from src import sql_code
except ImportError:
    from code import sql as sql_code

maps = {
        1: {
            "today": helpers.eightdigitdate,
            "six_mo_ago": helpers.six_months_ago,
            "personID": 250,
            },
        2: {
            }
            ,
        }

query_file = sys.argv[1]
if len(sys.argv)>2:
    mapping = sys.argv[2]
    try:
        mapping = maps[int(mappings)]
    except TypeError:
        mapping = json.loads(mapping)
else:
    mapping = dict(
        today= helpers.eightdigitdate,
        six_mo_ago= helpers.six_months_ago,
        personID= 250,
                   )

def get_rec(query_file=query_file, mapping=mapping):
#   part = parts[-1]
#   _ = input(f"{part=}")
#   f part == "f6": day = helpers.six_months_ago
#   lif part == "f": day = helpers.eightdigitdate
    with open(query_file, 'r') as stream:
        query = stream.read().format(**mapping)
    #_ = input(query)
    outfile = "query_output.csv"
    yn = input(f"Send data to {outfile}? (y/n): ")
    if yn and yn[0] in 'yY':
        sql_code.query2csv(query, outfile)
    else:
        print(sql_code.query_keys(query))
        res = sql_code.fetch(query, from_file=False)
        for line in res:
            print(line)



if __name__ == "__main__":
    print("Running run_query_w_map.py")
    get_rec()

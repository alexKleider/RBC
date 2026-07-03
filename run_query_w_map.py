#!/usr/bin/env python3

# File: run_query_w_map.py

"""
Provides a wrapper for ff_query2json
(which has been moved into code.sql.)

<file> (required param): the name of a file
containing a valid sql query, possibly with
{named} place holders, values for which must
be provided by either specifying an index
to [maps] or the name of a json file
as a second param.
So far only one map (indexed by 1)  is defined
and is the default.
"""


# When running from RBC:
# helpers found in code
# sql_code is code.sql 

import sys
import json
try: from src import helpers
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
            "appID": 250,
            "personID": 250
            },
        2: {
            }
            ,
        }

qfa = sys.argv[1]  # query file arg

if len(sys.argv)>2:
    mapping = sys.argv[2]
    try:
        mapping = maps[int(maps)]
    except TypeError:
        mapping = json.load(mapping)[0]
else:
    mapping = maps[1]

if __name__ == "__main__":
    print(f"Running run_query_w_map.py on {qfa}")
    j_file = "j_file2read.json"
    print(sql_code.ff_query2json(qfa, maps[1], j_file))


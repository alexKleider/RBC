#!/usr/bin/env python3

# File: stati.py

"""
Create a listing of the Stati table.
...by default goes to 'outf' (Notes/stati.txt.)
"""

import sys
from code import sql

outf = "Notes/stati.txt"
if len(sys.argv) > 2:
    p = True
else: p = False

query = """
SELECT statusID, key, text FROM Stati;
"""
res = sql.fetch(query, from_file=False)
with open(outf, 'w') as sink:
    sink.write("\n")
    sink.write("\n")
    sink.write("    Stati Table\n")
    sink.write("    ===========\n")
    sink.write("\n")

    for l in res:
        sink.write(
            f"{l[0]:>9}  {l[1]:.<10} {l[2]}" + "\n")
    print(f"Data sent to '{sink.name}'")
if p:
    for line in res:
        print(line)

if __name__ == "__main__":
    print("Running stati.py")

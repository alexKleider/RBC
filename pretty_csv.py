#!/usr/bin/env python3

# File: pretty_csv.py

"""
Accepts a csv file and makes it look better.
Perhaps this should be made into a function
and moved into ==> helpers
"""

import sys

args = sys.argv
if len(args) < 2:
    print("Must supply a file name.")
    sys.exit()
fname = args[1]
with open(fname, 'r') as infile:
    blob = infile.read()
#print(blob)
n = 0
numbers = []
data_array = []
#line_number = 0
data = blob.split("\n")
#for datum in data: print(datum)
#data_len = len(data)
#max_numbers = [0 for 
for line in data:
#   print(f"processing {line}")
    items = [item for item in line.split(",")]
    data_array.append(items)
    lengths = [len(item) for item in items]
    numbers.append(lengths)
#    line_number +=1

with open("array.txt", 'w') as arrayfile:
    for line in numbers:
        print(line, file=arrayfile)
max_nums = []
redact = '''
for index in range(len(lengths[0])):
    max_nums.append(max([len(lengths[index]) for index
'''


    

if __name__ == "__main__":
    pass
#   print("Running pretty_csv.py")

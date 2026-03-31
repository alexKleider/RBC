#!/usr/bin/env python3

# File: helpers.py

"""
A very stripped down version of helpers.py
used in other code bases.
"""

def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def tester():
    mapping1 = {"first": "Joe",
               'last': 'Blow',
               }
    mapping2 = {"first": "Joan",
               'last': 'Smith',
               }
    maps = [mapping1, mapping2]
    func = is_iterable

    fodder = [maps, func, ]

    for item in fodder:
        print("------------------")
        if is_iterable(item):
            for entry in item: print(entry)
        else:
            print(func.__name__)
    print("------------------")

if __name__ == "__main__":
    tester()

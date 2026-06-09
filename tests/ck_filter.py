#!/usr/bin/env python3

# File: ck_filter.py

"""
"""

def ok_set(set_, incl_set={}, excl_set={}):
    """
    Empty named parameters are ignored.
    Returns set_ if set_ includes in_set and
    does not include an item in ex_set.
    """
    if not incl_set: incl_set=set_
    if  not incl_set.isdisjoint(set_): # some overlap
        if excl_set.isdisjoint(set_):  # no overlap
            return True
    return False

l = [ 
     dict(submission= {3, 4, 5, 6},
          include={4,5,},
          exclude={1,2,},
          show="OK",
          ),
     dict(submission= {3, 4, 5, 6},
          include={1,5,},
          exclude={1,2,},
          show="notOK",
          ),
     dict(submission= {3, 4, 5, 6},
          include={4,5,},
          exclude={6,2,},
          show="notOK",
          ),
     dict(submission= {3, 4, 5, 6},
          include={1,4,5,},
          exclude={6,2,},
          show="notOK",
          ),
     ]

for m in l:
    if ok_set(m["submission"], m["include"], 
            m["exclude"]):
        print(m['show'])
    else:
        print(m['show'])



if __name__ == "__main__":
    print("Running ck_filter.py")

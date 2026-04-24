#!/usr/bin/env python3

# File: code/cli.py

"""
Provides the command line interface
(via the ui.py module.)
i.e. import cli as ui
"""

#print("code/cli.py: being imported (or run.)")
#print("!!!!!! run? !!!!!!!")

try:
    import helpers
except ImportError:
    from code import helpers


def yn(header="Confirmation Required",
       text="OK to proceed? (y/n"):
    """
    Returns True or False.
    <title> (ignored if None or empty) serves as a
    header which is printed and underlined ("=");
    """
    if header:
        print(header)
        print("=" * len(header))
    print(text)
    yn = input("Yes or No? (y/n) ")
    if yn and yn[0] in "yY":
        return True




def announce(header="Note the following...",
             text="Announcing..."):
    """
    Prints the header and the text
    and waits for 'go ahead' to proceed.
    """
    print("*"*len(header))
    print(header)
    print("*"*len(header))
    print(text)
#   _ = input("Any key to continue: ")


def ok(header="Confirmation Required",
       text="OK to proceed? (y/n"):
    """
    Returns True or False
    or possibly None if window is 'x'ed
    or if user response does not begin with
    one of the following letters: "yYnN".)
    """
    print("*"*len(header))
    print(header)
    print("*"*len(header))
    yn = input(text)
    if yn and yn[0] in "yY":
        return True
    if yn and yn[0] in "nN":
        return False
    return

def confirm_mapping(mapping, header="Confirmation Required",
                    text="Accept mapping as above? (y/n): "):
    print("*"*len(header))
    print(header)
    print("*"*len(header))
    for key, value in mapping.items():
        print(f"    {key}: {value}")
    yn = input(text)
    if yn and yn[0] in "yY":
        return True
    if yn and yn[0] in "nN":
        return False
    return


def choose(choices,
           header="Choose",
           text="(Select by number...)"):
    """
    <choices> must be a list of either functions or strings.
    Returns the chosen function or string.
    May return None (if choices is not an iterable,
                                is an empty list,
                             or if no choice is made.)
    Note: gui version selects the choice:
    the cli version, selects corresponding number.
    """
    ### Needs to utilise the header and text fields ###

    if not helpers.is_iterable(choices): return
    choices = [choice for choice in choices]
    if not choices: return
    _callable = callable(choices[0])
    if _callable:
        listing = [(count, item.__name__) for count,
            item in enumerate(choices, start=1)]
    else:
        listing = [(count, choice) for count, choice 
               in enumerate(choices, start=1)]
    while True:
        print("*"*len(header))
        print(f"{header}: {text}")
        for option in listing: print(f" {option}")
        message = "Choose one (0 to quit): "
        if _callable: 
            message = ("Choose a function to " +
                "execute (0 to quit): ")
        else:
            message = (
                f"Chose 0 to {len(choices)} (0 to quit): ")
        try:
            n = int(input(message))
        except ValueError:
            print("***")
            print("!!! Must be a number !!!")
            continue
        if n == 0: break  # returns None
        if n<0 or n>len(choices):
          print("***")
          print("!!! Number must be >=0 and " +
            f"<= {len(choices)} !!!")
          continue
        return choices[n-1]

def entries(mapping,
            header="Data Entry",
            text="Rtn to leave value as is, '_' to clear..."):
    while True:
            print("=" * len(header))
            print(header)
            print("=" * len(header))
            print(text)
            ret = {}
            for key, value in mapping.items():
                if value:
                    entry = input(f"{key}: {value}; New value: ")
                else:
                    entry = input(f"{key}: New value: ")
                if entry:
                    ret[key] = entry
                    if ret[key] == '_': ret[key] = ''
                else: ret[key] = value
            if ok(text="OK with above entries? (y/n) "):
                return ret
            if not ok(header="Try again?", text="y/n "):
                return


def add_info(mapping, *keys,
             header="Add/change values (_ reverses changes)",
             text="Can only change some..."):
    """        
    Key/Value pairs of <mapping> are presented but the
    user can only modify values of to the keys in <*keys>.
    Returns an updated version of the mapping.
    """
    while True:
        print("=" * len(header))
        print(header)
        print("=" * len(header))
        print(text)
        ret = {}
        for key, value in mapping.items():
            if key in keys:  # value can be changed
                if value:
                    entry = input(f"{key}: {value}; New value: ")
                else:
                    entry = input(f"{key}: Enter a value: ")
                if entry:
                    if entry == '_':  # revert to original
                        entry = mapping[key]
                    else:
                        entry = entry
                else: entry = ''  # clears the value
                ret[key] = entry
            else:  # key to an unchangeable value
                ret[key] = mapping[key]
                print(f"{key}: {value}  (Immutable!)")
        print("Current mapping...")
        for key, value in ret.items():
            print(f"{key}: {value}")
        if ok(text="OK with above entries? (y/n) "):
            return ret
        if ok(header="Try again?", text="y/n "):
            continue
        else:
            return
#               mapping = {key: value for key, value
#                          in ret.items()}


def get_hints(header="People Table Lookup",
              text="Enter hints"):
    """
    Returns a mapping of first, last, +/- suffix
    Do not enter wild cards- that's done elsewhere
    """
#   _ = input(f"running {__name__}.get_hints")
    while True:
        print("*"*len(header))
        print(header)
        print("*"*len(header))
        d = dict()
        d["first"] = input("Enter first name hint: ")
        d["last"] = input("Enter last name hint: ")
        d["suffix"] = input("Suffix hint (if any:) ")
        yn = input(f"OK with {d}? ")
        if yn and yn[0] in "yY":
            return d

def test_choose():
    choices = ['ying', 'yang', 'bang']
    ret = choose(choices,
                 header="Choose",
                 text="(Pick one by #)")
    print("testing 'choose' returned...")
    print(repr(ret))

def test_entries():
    mapping = {'first': 'alex',
               'last': 'kl',
               }
    ret = entries(mapping,
                  header="Data Entry",
                  text="Rtn to leave value as is...")
    print("Returning...")
    if not ret: print("Entry aborted!")
    else:
        for key, val in ret.items():
            print(f"{key}: {val}")

def ck_add_info():
    mapping = {1: 'alex', 2: "june", 3: "tanya",
               4: "kelly", 5: "gabriel", 6: 'frank'}
    keys = [5, 6]
    new_mapping = add_info(mapping, *keys)
    if new_mapping:
        print("returned new mapping...")
        for k, v in new_mapping.items():
            print(f"{k}: {v}")
    else:
        print(f"add_info returning {new_mapping}")

    
def main():
    test_choose()
    test_entries()
    pass

if __name__ == "__main__":
    print("Running code/cli.py")
#   main()
    ck_add_info()

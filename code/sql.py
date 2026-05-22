#!/usr/bin/env python3

# File: code/sql.py

"""
SQL(ite3) helper code.
Code involving specific queries should be in code/data.py
"""

import os
import csv
import shutil
import sqlite3
try: import helpers
except ImportError: from code import helpers

db_file_name = "/home/alex/Git/RBC/Data/club.db"

def initDB(path):
    """
    Returns a connection ("db")
    and a cursor ("clubcursor")
    """
    try:
        db = sqlite3.connect(path)
        clubcursor = db.cursor()
    except sqlite3.OperationalError:
        print("Failed to connect to database:", path)
        db, clubcursor = None, None
        raise
    return db, clubcursor


def closeDB(database, cursor):
    try:
       cursor.close()
       database.commit()
       database.close()
    except sqlite3.OperationalError:
       print( "problem closing database..." )
       raise

note2self = """
# might want to make "partial function"(s) out of the fetch function:
https://www.kdnuggets.com/partial-functions-in-python-a-guide-for-developers
"""

def fetch(sql_source, db=db_file_name, params=None, data=None,
                    from_file=True, commit=False,
                    verbose=False):
    """
    <sql_source> must be a string: either the name of a file
    containing a valid sqlite3 query or (if <from_file> is set
    to False) the query itself. The query is executed on the <db>.
    Only one (if any) of the following should be provided:
        <params> must be an iterable of length to match number
            of qmark placeholders in the query. Remember to use
            the '%' character as a suffix (or prefix or both.)
        <data> must be a dict with all keys necessary to match
            all place holders in the query. Remember place holder
            names are prefaced by a colon in the query.
            eg: (:key1, :key2).
    Be aware that the query might return an empty list.
    """
    if from_file:
        with open(sql_source, 'r') as source:
            query = source.read()
#       _ = input(f"### Query begins next line\n{query}")
    else: query = sql_source
    if verbose:
        print("Query being called is...")
        _ = input(query)
    db, cur = initDB(db)
    if data:
        cur.executemany(query, data)
    elif params:
#       _ = input(f"params set to '{params}'")
        cur.execute(query, params)
    else:
        cur.execute(query)
#   _ = input(
#       f"get_query_result returning the following:\n {ret}")
    ret = cur.fetchall()
    if commit:
        db.commit()
        if verbose:
            _ = input("Committed!")
    closeDB(db, cur)
    if verbose:
        print(f"routines.fetch returning {ret}")
    return ret

def import_query(sql_file_name):
    """
    Returns the content of <sql_file_name>
    (assumed to be a text file.)
    Typically used for queries that require formatting.
    """
    with open(sql_file_name, 'r') as inf:
        return(inf.read())

def fetch_d_query(sql_file_name, data, commit=False):
    """
    Assumes <sql_file_name> is a file containting an SQL query
    with place holders keyed by key/value pairs available
    in <data>, a dict.
    """
    query = import_query(sql_file_name)
    query = query.format(**data)
#   _ = input(f"fetch_d_query param is\n{query}")
    return fetch(query, from_file=False, commit=commit)


def looseSQLcomments(query_text):
    """
    Returns sql query devoid of  comments.
    """
    # first get rid of the /*..*/ comments:
    b = query_text.find("/*")
    while b > -1:
        e = query_text.find("*/")
        if not e > b:
            print(
            "!!!Unmatched /*..*/ in looseSQLcomments!!!")
            assert False
        query_text = query_text[:b] + query_text[e+2:]
        b =query_text.find("/*")
    # now get rid of those prefaced by "--"
    lines = []
    for line in query_text.split("\n"):
        line = line.strip()
        n = line.find("--")
        if n > -1:
            line = line[:n]
        lines.append(line)
    return "\n".join(lines)


def keys_from_schema(table, brackets=(0,0)):
    """
    query comes from: https://stackoverflow.com/questions/11996394/is-there-a-way-to-get-a-schema-of-a-database-from-within-python
    <brackets> provides ability to ignore first brackets[0]
    and last brackets[1] primary keys such as 'personID' (in
    which case it can be set to (1,0).
    Tested in tests/test_routines.py
    """
    query =  f"pragma table_info({table})"
    res = fetch(query, from_file=False)
    end = brackets[1]
    if not end:
        ret = [item[1] for item in
             res[brackets[0]:]]
    else:
        ret = [item[1] for item in
             res[brackets[0]:end]]
    # item[1] is the column/key.
    return ret


def keys_from_query(query, replace_periods=False):
    """
    Returns a listing of keys requested in the query
    Able to deal with "SELECT * FROM .." queries.
    If 'replace_periods' is set to True: replace with "_"
    otherwise remove prefix and period.
    """
    query = looseSQLcomments(query)
    nselect = query.find("SELECT")
    nfrom = query.find("FROM")
    keystring = query[nselect+6:nfrom]
    if keystring.strip() == "*":
        words = query.split()
        table = words[3].strip(';')
        return keys_from_schema(table)
    nowhitespace = ''
    for ch in keystring:
        if ch.split():
            nowhitespace = nowhitespace + ch
    keys = nowhitespace.split(",")
    if replace_periods:
        return [key.replace('.', '_') for key in keys]
    else:
        splitkeys = [key.split('.') for key in keys]
        return [key[-1] for key in splitkeys]


def dicts_from_query(query, from_file=False,
                     keys=None, replace_periods=False):
    """
    A generator function yielding dicts.
    If <keys> are not provided, uses <keys_from_query()>.
    Use query2dict_listing if a list is needed.
    """
#   print(f"dicts_from_query has from_file set to {from_file}")
    if from_file:
        with open(query, 'r') as q_file:
            query = q_file.read()
#   print(f"in dicts_from_query, query is\n{query}")
    if not keys:
        keys = keys_from_query(query,
                       replace_periods=replace_periods)
#   print(f"in dicts_from_query keys are.../n{keys}")
    res = fetch(query, from_file=False)
#   _ = input(res)
    for entry in res:
        d = dict(zip(keys, entry))
        yield d


def query2dict_listing(query, keys=False,
                       from_file=False):
    """
    Returns query result as a (could be empty!) list of dicts
    (which can be dumped into a json file.)
    A listing of <keys> can be supplied; defaults to a call
    to keys_from_query. A call to keys_from_query is another
    way the user can generate the listing.
    Fails if len(keys)!=length of tupples
    """
    if from_file:
        query = import_query(query)
    ret = []
    if not keys:
        keys = keys_from_query(query)
    res = fetch(query, from_file=from_file)
    for entry in res:
        d = dict(zip(keys, entry))
        ret.append(d)
    return ret


def query2dicts(query, from_file=False):
    """
    SHOULD BE REDACTED in favour of query2dict_listing()
    Returns a (possibly empty) list of dicts.
    """
    if from_file:
        query = import_query(query)
    return query2dict_listing(query,
            keys_from_query(query))


def table2csv(table, fname):
    """
    Prints all entries in <table>
    to <fname>.
    """
    keys = keys_from_schema(table)
    query = f"SELECT * FROM {table};"
    with open(fname, 'w', newline='') as stream:
        dictwriter = csv.DictWriter(stream, keys)
        dictwriter.writeheader()
        for mapping in dicts_from_query(query,
                                        keys=keys):
            dictwriter.writerow(mapping)

def query2csv(query, fname):
    """
    <query> is text of query.
    Results of the query go to <fname>
    """
#   keys = keys_from_query(query)
    keys = query_keys(query)
    with open(fname, 'w', newline='') as stream:
        dictwriter = csv.DictWriter(stream, keys)
        dictwriter.writeheader()
        for mapping in dicts_from_query(query,
                                        keys=keys):
#           _ = input(repr(mapping))
            dictwriter.writerow(mapping)

def query_keys(query):
    """
    Accepts a <query> and returns keys to the values expected to be
    returned. The "." in "dot" keys (ie P.name) are converted to "_".
    """
    query = query.replace(";", " ")
    ib = query.find("SELECT")
    ie = query.find("FROM")
    ls = len("SELECT")
    if not(ib>=0 and ie>0 and ((ie - ib) > ls)):
        print(f"not({ib}>=0 and {ie}>0 and (({ie} - {ib}) > {ls}))")
        print("Unable to select keys from query!!!")
        assert False
    keystring = query[ib+len("SELECT"):ie].strip()
    if keystring == "*":
        begin = ie + len("FROM") + 1
        end = query.find(" ", begin)
        table = query[begin:end].strip()
        return keys_from_schema(table)
    nowhitespace = ''
    for ch in keystring:
        if ch.split():
            nowhitespace = nowhitespace + ch
    keys = nowhitespace.split(',')
    return  [key.replace(".", "_") for key in keys]

def db2csv(report=None):
    """
    Backs up the data base (Data/club.db) by creating a csv file
    for each table, putting them all into a separate directory,
    and then creating a zip file to be backed up on Google Drive.
    """
    if not report:
        report = []
    tempdir = "TempZIP_Dir"
    zip_name = f"{helpers.eightdigitdate4filename}_db_as_CSVs"
    tables = fetch(
            """SELECT name FROM sqlite_master
               WHERE type='table';""", from_file=False)
    tables = [table[0] for table in tables]
    os.mkdir(tempdir)
    for table in tables:
        file_name = tempdir +'/' + f"{table}.csv"
        keys = keys_from_schema(table)
        with open(file_name, 'w', newline='') as stream:
            csv_writer = csv.writer(stream)
            csv_writer.writerow(keys_from_schema(table))
            res = fetch(f"SELECT * FROM {table};",
                    from_file=False)
            for row in res:
                csv_writer.writerow(row)
    archived = shutil.make_archive(zip_name, 'zip', tempdir)
    report.append("created: " + repr(archived))
    print(report[-1])
    shutil. rmtree(tempdir)
    return report

redact = '''
## should not all of the following
## be moved to  code/data.py???
## none of them appear to be used in code/
##   reports, logic, or data !!!!!!!!

def dict_from_list(listing, fields):
    """
    <listing> is an iterable as might be an element in what's
    returned by an SQL query.
    <fields> is an array of (word, integer, ) tuples that
    determines which entry in the listing is keyed by what
    <word> in the resulting dict.
    """
    ret = {}
    for word, i in fields:
        ret[word] = listing[i]
    return ret
def get_demographic_dict(personID):
    """
    Wrongly???  Moved from code/dates.py
    If a valid personID is provided returns a dict
    keyed by <keys> (see code below.)
    If invalid personID: returns None
    """
    keys = ("personID first last suffix address town " +
            "state postal_code country email")
    key_listing = keys.split()
    fields = ', '.join(key_listing)
    query = f"""
        SELECT {fields}
        FROM People 
        WHERE personID = {personID};
    """
    res = fetch(query, from_file=False)
    if not res or not res[0]:
        return
    return helpers.make_dict(key_listing, res[0])

def get_person_fields_by_ID(personID, fields=None):
    """
    Select values of the <fields> columns from the People table
    for the personID specified.
    Returns a dict keyed by names of fields
    `_if_ <fields> is provided (as an iterable,)
     _otherwise_ returns a tuple of all fields.
    """
#   _ = input("Entering code/routines.get_person_fields_by_ID")
    query = """SELECT {{}} FROM People
    WHERE personID = {};""".format(personID)
    if fields:
        fields = [field for field in fields]
        var = ', '.join(fields)
    else: var = '*'
    query = query.format(var)
#   _ = input(query)
    res = fetch(query, from_file=False)[0]  # Note the '[0]'
    if fields:
        dic = {}
        z = zip(fields, range(len(fields)))
        for field, n in z:
            dic[field] = res[n]
#       for key, value in dic.items():
#           print(f"'{key}': '{value}'")
#       _ = input("^dict version of query^")
        return dic
    else:
#       _ = input(res)
        return res

def get_ids_by_name(first, last, db=db_file_name):
    """
    Returns People.personID (could be more than one!)
    for anyone with <first> <last> name.
    Returns a (possible empty) tuple.
    Unlikely it'll ever be more than a tuple with one value
    """

    query = f"""SELECT personID, first, last, suffix from People
            WHERE People.first = "{first}"
            AND People.last = "{last}" """
#   _ = input(query)
    con = sqlite3.connect(db)
    cur = con.cursor()
    execute(cur, con, query)
    res = cur.fetchall()
    if not res:
        _ = input("No key for {} {}".format(first, last))
    return res


def get_people_fields_by_ID(db_file_name=db_file_name,
                                    fields=None):
    """
    ## What is this for???
    Select values of the <fields> columns from the People table.
    Default (<fields> not specified) is to select all fields.
    """
    ret = {}
    query = """SELECT {} FROM People;"""
    if fields:
        fields = ["personID", ] + [field for field in fields]
        var = ', '.join(fields)
    else: var = '*'
    query = query.format(var)
#   _ = input(query)
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur, con, query.format(var))
    res = cur.fetchall()
#   _ = input(res)
    for entry in res:
        ret[entry[0]] = entry[1:]
    return ret


def get_name(personID):
    if not personID:
        return ""
    name_query = """SELECT first, last, suffix
            FROM People
            WHERE personID = ?;"""
    res = fetch(name_query, f'{db_file_name}',
            from_file=False, params=[personID, ])[0]
    suffix = res[2]
    if suffix:
        suffix = f" {suffix}"
    return "{0:} {1:}".format(*res) + suffix


def id_by_name():
    """
    Returns a listing of strings: '{Id} {first} {last} {suffix}'
    from the 'People' table.
    Prompts for first letter(s) of first &/or last name(s).
    If both are blank, none will be returned!
    """
    query = """
    SELECT personID, first, last, suffix
    FROM People
    WHERE {}
    ;
    """
    print("Looking for people:")
    print("Narrow the search...")
    first = input("  First name (partial or blank): ")
    last = input( "   Last name (partial or blank): ")
    if first and last:
        query = query.format("first LIKE ? AND last LIKE ? ")
    elif first:
        query = query.format("first LIKE ?")
    elif last:
        query = query.format("last LIKE ? ") 
    else:  # no entry provided
        return
    params = [name+'%' for name in (first, last,) if name]
    ret = fetch(
                query,
                params=params,
                data=None,
                from_file=False,
                commit=False
                )
    ret = ["{:3>} {} {} {}".format(*entry) for entry in ret]
#   _ = input(ret)
    return ret

def pick_id():
    """
    Returns a chosen personID or None.
    """
    while True:
        listing = id_by_name()
        if not listing:
            print("No matches")
            return
        print("Pick an ID from the following (0 to abort):")
        choices = []
        for entry in listing:
            choices.append(entry.split()[0])
            print("    " + f"{entry}")
        while True:
            choice = input("Which ID do you want? (0 to abort): ")
            if choice == "0":
                print("Aborting!")
                return
            if choice in choices:
                return int(choice)
            else:
                print("You made a non-listed choice!")
                yn = input("Continue with '{choice}'? (yn): ")
                try:
                    choice = int(choice)
                except ValueError:
                    print("Must be a personID; starting over!")
                    break
                if yn and yn[0] in "yY":
                    return int(choice)



people_query = """/* Sql/get_by_ID_f.sql */
        SELECT * FROM People WHERE personID = {};
        """
like_query = """
        SELECT * FROM People WHERE {};
        """

def get_rec_by_ID(ID):
    """
    Returns a record corresponding to personID if record
    exists, otherwise returns None
    (Client is pick_People_record)
    """
    res = fetch(people_query.format(ID), from_file=False)
#   _ = input(res)
    if not res:
        return
    ret = helpers.make_dict(
            keys_from_schema("People"), res[0])
#                               from_file=False)
    if not ret:
        return
    else:
        return ret


def pick_People_record(header_prompt=None, report=None):
    """
    Returns either a dict representing a person in the People
    table...  or None.
    Prompts for name clues (which can be ignored)
    #?Makes id_by_name() redundant??
    """
    if isinstance(report, list):
        report.append(
                "... entering routines.pick_People_record()")
    keys = keys_from_schema("People")
    if header_prompt: print(header_prompt)
    while True:
        print(
          "Narrow the search (blanks if ID known)...")
        first = input("First name (partial or blank): ")
        last = input("Last name (partial or blank): ")
        if first and last:
            query2use = like_query.format(
                f"""first LIKE "{first}%" AND last LIKE "{last}%" """)
        elif first:
            query2use = like_query.format(
                    f"""first LIKE "{first}%" """)
        elif last:
            query2use = like_query.format(f"""last LIKE "{last}%" """) 
        else:  # no entry provided
            query2use = listing = None
        if query2use:
            res = fetch(
                    query2use,
                    from_file=False,
                    )
            listing = [helpers.make_dict(keys, entry)
                                    for entry in res]
        if listing:
            choices = [d['personID'] for d in listing]
            print("Choose an ID from one of the following:")
            for d in listing:
                print("{personID:3>} {first} {last} {suffix}"
                                            .format(**d))
        ID = input("Enter a personID (0 to exit):  ")
        try:
            ID = int(ID)
        except ValueError:
            helpers.add2report(report, 
                "..non integer entered; restarting..",
                also_print=True)
            if report: print(report[-1])
            continue
        else:
            if ID == 0:
                if isinstance(report, list):
                    report.append(
                    "... '0' entry ==> exit pick_People_record.")
                return
        if listing and ID in choices:
            for d in listing:
                if d['personID'] == ID:
#                   print(f"returning: {d}")
                    if isinstance(report, list):
                        report.append(
                            f"pick_People_record => \n{repr(d)}")
                    return d
        else:
            rec = get_rec_by_ID(ID)
            if not rec:
                if isinstance(report, list):
                    report.append(
                        "... no such ID: starting over ..")
                continue
            else:
                if isinstance(report, list):
                    report.append(
                        "... pick_People_record => a dict.")
                return rec

'''


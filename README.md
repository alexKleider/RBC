
# File: README.md

# RBC

Code (rewrite of Git/Sql) to support data management
by the Membership Chair of the Bolinas Rod & Boat Club

An attempt this time is to follow MVC priniples although
it proved impossible to stick to it regorously!

Layers used are: 
    * code/data 
        Deals with the data base.
        Currently using Sqlite3 (see code/data/sql.py)
    * code/logic
        The logic layer
        Relys on data layer to store and retrieve data
        Still needs the interface layer to collect date!
    * code/ui  (cli or gui modules imported as ui)
        The user interface
    * main
        The driver program although it can be driven by logic
App_mapping keys are:
    first: Joe
    last: Schmo
    suffix: 
    phone: 868
    address: Elm
    town: Bo
    state: CA
    postal_code: 949
    country: usa
    email: js@mail
    personID: 253
    app_rcvd: 20260408
    fee_rcvd: 20260428
    meeting1: 
    s1_ID: 97
    s2_ID: 35
    s1_first
    s1_last
    s1_suffix
    s1_email
    s2_first
    s2_last
    s2_suffix
    s2_email


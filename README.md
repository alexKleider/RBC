
# File: README.md

# RBC

A code (rewrite of Git/Sql) to support data management
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



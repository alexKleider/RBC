
# File: README.md

# RBC

Code (rewrite of Git/Sql) to support data management
by the Membership Chair of the Bolinas Rod & Boat Club

An attempt this time is to follow MVC priniples although
it proved impossible to stick to it regorously!

Layers used are: 
    * code/data 
        Deals with the data base via the sql.py module
        Currently using Sqlite3 (see code/data/sql.py)
    * code/logic
        The logic layer
        Relys on data layer to store and retrieve data
        Still needs the interface layer to collect date!
    * code/ui  (cli or gui modules imported as ui)
        The user interface
    * main
        The driver program although it can be driven by logic

App_mapping keys are:  (See Sql/all_applicants_f.sql)
    PS_statusID, A_app_rcvd, S1_personID, S2_personID,
    P_personID,  A_fee_rcvd, S1_first,    S2_first,
    P_last,      A_meeting1, S1_last,     S2_last,
    P_first,     A_meeting2, S1_suffix,   S2_suffix,
    P_suffix,    A_meeting3, PS1_statusID,PS2_statusID,
    P_phone,     A_approved,,
    P_address,   A_dues_paid,
    P_town,      A_notified,
    P_state,
    P_postal_code,
    P_email,


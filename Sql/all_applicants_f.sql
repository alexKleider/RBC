/* Sql/all_applicants_f.sql
-- was called (replaces) Sql/appl_dates_sponsors_f.sql
-- Returns listing of all data for all current applicants
-- Requires {today} to be specified  */
SELECT
    P.personID, PS.statusID, P.last, P.first, P.suffix,
    P.phone, P.address, P.town, P.state, P.postal_code,
    P.email,
    A.app_rcvd, A.fee_rcvd, A.meeting1, A.meeting2, A.meeting3,
    A.approved, A.dues_paid, A.notified
    S1.first, S1.last, S1.suffix, S1.personID, PS1.statusID,
    S2.first, S2.last, S2.suffix, S2.personID, PS2.statusID
FROM 
     People AS P,  --the applicant  |
     People AS S1, --sponsor #1     | people table
     People AS S2, --sponsor #2     |
     Applicants AS A, -- the applicant table
     Person_Status as PS,  -- applicant  |
     Person_Status as PS1, -- sponsor1   | Person_Status table
     Person_Status as PS2  -- sponsor2   |
WHERE P.personID = A.personID  -- Person and Applicant tables
AND   P.personID = PS.personID  -- Person and Person_Status
AND   S1.personID = A.sponsor1ID
AND   PS1.personID = S1.personID
AND   PS1.statusID < 20
AND   PS1.end = ""
AND   PS2.personID = S2.personID
AND   S2.personID = A.sponsor2ID
AND   PS2.statusID < 20
AND   PS2.end = ""
AND   (PS.end = "" OR PS.end > {today})
AND   PS.statusID < 11
AND   A.notified = ""
ORDER BY 
    P.personID ASC
;
/* App_mapping keys are:  (See README.md)
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
  */

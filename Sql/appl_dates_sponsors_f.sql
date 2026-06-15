/* Sql/appl_dates_sponsors_f.sql */
-- Requires {today} to be specified 
SELECT
    P.personID, PS.statusID, P.last, P.first, P.suffix,
--  P.phone, P.address, P.town, P.state, P.postal_code,
--  P.email,
    Ap.app_rcvd, Ap.meeting1, Ap.meeting2, Ap.meeting3,
    S1.first, S1.last, S1.suffix, S1.personID, PS1.statusID,
    S2.first, S2.last, S2.suffix, S2.personID, PS2.statusID
    -- check sponsor statusID ?member in good standing?
FROM 
     People AS P,  --the applicant  |
     People AS S1, --sponsor #1     | people table
     People AS S2, --sponsor #2     |
     Applicants AS Ap, -- the applicant table
     Person_Status as PS,  -- applicant  |
     Person_Status as PS1, -- sponsor1   | Person_Status table
     Person_Status as PS2  -- sponsor2   |
WHERE P.personID = Ap.personID  -- Person and Applicant tables
AND   P.personID = PS.personID  -- Person and Person_Status
AND   S1.personID = Ap.sponsor1ID
AND   PS1.personID = S1.personID
AND   PS1.statusID < 20
AND   PS1.end = ""
AND   PS2.personID = S2.personID
AND   S2.personID = Ap.sponsor2ID
AND   PS2.statusID < 20
AND   PS2.end = ""
AND   (PS.end = "" OR PS.end > {today})
AND   PS.statusID < 11
AND   Ap.notified = ""
ORDER BY 
    P.personID ASC
;


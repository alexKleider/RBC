/* Sql/appl_w_sponsors_f.sql */
-- Requires {today} to be specified 
SELECT
    P.personID, PS.statusID, P.last, P.first, P.suffix,
--  P.phone, P.address, P.town, P.state, P.postal_code,
--  P.email,
    At.meeting1,
    S1.first, S1.last, S1.personID, PS1.statusID,
    S2.first, S2.last, S2.personID, PS2.statusID
FROM 
     People AS P,  --the applicant  |
     People AS S1, --sponsor #1     | people table
     People AS S2, --sponsor #2     |
     Applicants AS At, -- the applicant table
     Person_Status as PS,  -- applicant  |
     Person_Status as PS1, -- sponsor1   | Person_Status table
     Person_Status as PS2  -- sponsor2   |
WHERE P.personID = At.personID  -- Person and Applicant tables
AND   P.personID = PS.personID  -- Person and Person_Status
AND   S1.personID = At.sponsor1ID
AND   PS1.personID = S1.personID
AND   PS1.statusID < 20
AND   PS1.end = ""
AND   PS2.personID = S2.personID
AND   S2.personID = At.sponsor2ID
AND   PS2.statusID < 20
AND   PS2.end = ""
AND   (PS.end = "" OR PS.end > {today})
AND   PS.statusID < 11
--ORDER BY P.last, P.first, P.suffix
ORDER BY PS.statusID ASC, P.personID ASC
;


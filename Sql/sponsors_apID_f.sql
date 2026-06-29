/* Sql/sponsors_apID_f.sql */
-- Requires applicant's ID to be specified
-- Returns sponsor data.

SELECT 
    S1.personID, S1.first, S1.last, S1.email,
    S2.personID, S2.first, S2.last, S2.email
FROM 
     People AS S1, --sponsor #1     | people table
     People AS S2, --sponsor #2     |
     Applicants AS Ap -- the applicant table
WHERE Ap.personID = {A_personID}
AND   S1.personID = Ap.sponsor1ID
AND   S2.personID = Ap.sponsor2ID
;

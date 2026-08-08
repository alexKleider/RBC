/* File: Sql/sponsors.sql
--Requires personID to be provided.
--Provides sponsor data for Applicant table entry
specified by {personID}.
-- Developed in place of Sql/id2appl_mapping.sql
which has been deleted.
*/
SELECT
    P.personID, P.first, P.last, P.suffix,
    P.phone, P.address, P.town, P.state,
    P.postal_code, P.country, P.email,
--  A.app_rcvd, A.fee_rcvd, A.meeting1, A.meeting2,
--  A.meeting3, A.approved, A.dues_paid, A.notified,
    S1.first, S1.last, S1.suffix, S1.email,
    S1.personID,
    S2.first, S2.last, S2.suffix, S2.email,
    S2.personID 
FROM People AS P, Applicants AS A,
    People AS S1, People AS S2

WHERE P.personID = {personID}    AND A.personID = P.personID
AND  S1.personID = A.sponsor1ID  AND S2.personID = A.sponsor2ID
;

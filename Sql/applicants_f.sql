/* Sql/applicants_f.sql

    Requires {today} to be a key provided by
    the dict supplied to code/sql.fetch_d_query()
*/
SELECT
    P.personID, P.last, P.first, P.suffix,
    P.phone, P.address, P.town, P.state, P.postal_code, P.email,
    sponsor1ID, sponsor2ID, PS.begin
FROM Applicants AS Ap,
     People AS P,
     Person_Status as PS
WHERE Ap.personID = P.personID
AND   Ap.personID = PS.personID
AND   PS.statusID < 11
AND   (PS.end = "" OR PS.end > {today})
--ORDER BY P.last, P.first, P.suffix
ORDER BY Ap.personID
;
/* returns:
personID, last, first, suffix, phone, address, town, state,
postal_code, email, sponsor1, sponsor2, personID, begin, end
*/


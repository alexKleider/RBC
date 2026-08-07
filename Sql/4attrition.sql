/*
# File: Sql/4attrition.sql

*/

SELECT P.first, P.last, P.suffix,
        PS.statusID, PS.begin, S.text
FROM People as P,
     Person_Status as PS,
     Stati as S
WHERE
    P.personID = PS.personID
AND PS.statusID = S.statusID
AND PS.statusID in (18, 26, 27, 28)
AND PS.end = ""
ORDER BY PS.begin
;


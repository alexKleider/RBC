/* File: Sql/leadership_f.sql
-- already using P_ prefix for People table,
-- PS for Person_Status table
-- and S for Stati table.
-- Requires formatting of {today}.  */


SELECT
    S.text, S.statusID, PS.begin, PS.end,
     P.personID, P.first, P.last, P.suffix
FROM People as P
JOIN Person_Status as PS 
ON PS.personID = P.personID 
JOIN Stati as S
ON PS.statusID = S.statusID
WHERE
PS.statusID in (20, 21, 22, 23, 24, 25,
                31, 32, 33, 34, 35)
AND (
    PS.end >= {today}
    OR PS.end = ''
    )
order by PS.statusID, P.last;

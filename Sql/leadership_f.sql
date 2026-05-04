-- File: Sql/leadership_f.sql

SELECT P.personID, P.first, P.last, P.suffix,
    S.statusID,
    S.text, PS.begin, PS.end
    FROM People as P
JOIN Person_Status as PS 
ON PS.personID = P.personID 
JOIN Stati as S
ON PS.statusID = S.statusID
WHERE
PS.statusID in (20, 21, 22, 23, 24, 25)
AND (
    PS.end >= {today}
    OR PS.end = ''
    )
order by PS.statusID, P.last;

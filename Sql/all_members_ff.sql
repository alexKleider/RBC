/* Sql/all_members_ff.sql */
-- !! Requires formatting: {today} = eightdigitdate x2!!
SELECT
    P.personID, PS.statusID,
    P.first, P.last, P.suffix, P.email, P.address,
    P.town, P.state, P.postal_code, P.phone,
    PS.begin
FROM
    People AS P
JOIN
    Person_Status AS PS
ON
    P.personID = PS.personID
WHERE
     PS.statusID in (11, 15, 14, 16, 17)
AND (PS.begin = '' OR PS.begin <= '{today}')
AND (PS.end = '' OR PS.end > '{today}')
ORDER BY
    P.last, P.first, P.suffix
;


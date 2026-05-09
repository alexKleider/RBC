/* File: Sql/expired_f6.sql (31 * 6 = 186) */

SELECT P.personID, P.first, P.last, P.suffix,
        S1.first, S1.last, S1.suffix,
        S2.first, S2.last, S2.suffix,
        A.meeting1
FROM People as P,
     People as S1,
     People as S2,
     Applicants as A
WHERE A.personID = P.personID
AND   A.sponsor1ID = S1.personID 
AND   A.sponsor2ID = S2.personID
AND   A.meeting1 < {day}
AND   A.meeting3 = ""
AND   A.notified = ""
;

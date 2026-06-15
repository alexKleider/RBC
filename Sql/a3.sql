/* Sql/a3.sql */

/* See docstring for code/ck_data.ck_appl_vs_status_tables()
Applicants who've attended three meetings. */
-- may wish to change ORDERing. ie by dates

SELECT P.personID, P.first, P.last, P.suffix
FROM People     AS P
JOIN Applicants  AS A
ON A.personID = P.personID
WHERE A.notified = ""  -- exclude non applicants
  AND A.meeting1 != ""
  AND A.meeting2 != ""
  AND A.meeting3 != ""
  AND A.approved = ""
  AND A.notified = ""
ORDER BY P.last, P.first, P.suffix
;

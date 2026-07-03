/* Sql/still_applicants.sql */

SELECT  P.personID, P.last, P.first, P.suffix,
        A.app_rcvd, A.fee_rcvd,
        A.meeting1, A.meeting2, A.meeting3,
        A.approved, A.dues_paid, A.notified
FROM People  AS P
JOIN Applicants AS A   ON A.personID = P.personID
WHERE A.notified = '' -- still an applicant
--ORDER BY P.last, P.first
ORDER BY A.app_rcvd, A.meeting3, A.meeting2,
        A.meeting1, A.fee_rcvd
;


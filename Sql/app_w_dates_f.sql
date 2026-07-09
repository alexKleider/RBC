/* Sql/app_w_dates_f.sql
    Provides demographics and dates based on 
    applicant's known personID
*/
SELECT
    P.personID, P.last, P.first, P.suffix,
    P.phone, P.address, P.town, P.state,
    P.postal_code, P.email,
    A.app_rcvd, A.fee_rcvd, A.meeting1, A.meeting2,
    A.meeting3, A.approved, A.dues_paid, A.notified
FROM Applicants AS A,
     People AS P
WHERE P.personID = {personID} -- id_
AND   A.personID = P.personID
;


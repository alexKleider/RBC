/* Sql/app_w_dates_f.sql
    Provides demographics and dates based on 
    applicant's known personID
*/
SELECT
    A.personID, A.last, A.first, A.suffix,
    A.phone, A.address, A.town, A.state,
    A.postal_code, A.email,
    AP.app_rcvd, AP.fee_rcvd, AP.meeting1, AP.meeting2,
    AP.meeting3, AP.approved, AP.dues_paid, AP.notified
FROM Applicants AS AP,
     People AS A
WHERE A.personID = {} -- id_
AND   AP.personID = A.personID
;


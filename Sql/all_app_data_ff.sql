/* Sql/all_app_data_ff.sql
* requires a mapping value for "personID" & for "today"
- could replace: Sql/app_w_dates_f.sql
               & Sql/appl_w_sponsors_f.sql            */
SELECT
    A.personID, A.last, A.first, A.suffix,
    A.phone, A.address, A.town, A.state,
    A.postal_code, A.country, A.email,
    AP.app_rcvd, AP.fee_rcvd, AP.meeting1, AP.meeting2,
    AP.meeting3, AP.approved, AP.dues_paid, AP.notified,
    ApS.statusID,  -- St.key, St.text,
    S1.first, S1.last, S1.suffix, S1.personID, -- PS1.statusID,
    S2.first, S2.last, S2.suffix, S2.personID  -- PS2.statusID
FROM People AS A, Applicants AS AP,
    People AS S1, People AS S2,
    Person_Status AS ApS, Person_Status AS PS1,
    Person_Status AS PS2,
    Stati AS St
WHERE A.personID = {personID}    AND  AP.personID = A.personID
AND  S1.personID = AP.sponsor1ID AND  S2.personID = AP.sponsor2ID
AND  ApS.personID = A.personID   AND  AP.notified = ""
AND  ApS.begin < {today}         AND  ApS.end = ""
AND  ApS.statusID = St.statusID
AND  PS1.personID = S1.personID  AND  PS2.personID = S2.personID
AND  PS1.end = ""                AND  PS2.end = ""
;

    

    


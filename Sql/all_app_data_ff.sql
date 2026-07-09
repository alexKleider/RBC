/* Sql/all_app_data_ff.sql
* requires a mapping value for "personID" & for "today"
- could replace: Sql/app_w_dates_f.sql
               & Sql/appl_w_sponsors_f.sql
Should change People AS A to People as P!!          */
SELECT
    P.personID, P.last, P.first, P.suffix,
    P.phone, P.address, P.town, P.state,
    P.postal_code, P.country, P.email,
    AP.app_rcvd, AP.fee_rcvd, AP.meeting1, AP.meeting2,
    AP.meeting3, AP.approved, AP.dues_paid, AP.notified,
    ApS.statusID,  -- St.key, St.text,
    S1.first, S1.last, S1.suffix, S1.personID, -- PS1.statusID,
    S2.first, S2.last, S2.suffix, S2.personID  -- PS2.statusID
FROM People AS P, Applicants AS AP,
    People AS S1,           People AS S2,
    Person_Status AS ApS,   Stati AS St,
    Person_Status AS PS1,   Person_Status AS PS2

WHERE P.personID = {personID}    AND AP.personID = P.personID
AND  S1.personID = AP.sponsor1ID AND S2.personID = AP.sponsor2ID
AND  ApS.personID = P.personID   AND AP.notified = ""
AND  ApS.begin < "{today}"       AND ApS.end = ""
AND  ApS.statusID = St.statusID
AND  PS1.personID = S1.personID  AND PS2.personID = S2.personID
AND  PS1.statusID = 15           AND PS2.statusID = 15
AND  PS1.begin < "{today}"       AND PS1.begin < "{today}"
AND (PS1.end = ""                 OR PS1.end > "{today}")
AND (PS2.end = ""                 OR PS2.end > "{today}")
;

    

    


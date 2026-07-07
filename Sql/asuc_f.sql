/* Sql/asuc_f.sql  Applicant Satus update close
-- updates/closes current status  -format x1 only
Uses A_ prefix, should change to P_personID
Also consider {status2close}
*/
UPDATE Person_Status SET
    end = {date}
WHERE personID = {A_personID}
  AND statusID = {status2close}
    ;

/* Sql/asuc_f.sql  Applicant Satus update close */
-- updates/closes current status  -format x1 only

UPDATE Person_Status SET
    end = {date}
WHERE personID = {A_personID}
  AND statusID = {status2close}
    ;

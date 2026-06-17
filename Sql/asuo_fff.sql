/* Sql/asuo_fff.sql  Applicant Satus update open */
-- creates (opens) a new entry  -format x3

INSERT INTO Person_Status
        (personID, statusID, begin)
VALUES ({personID}, {status2open}, {date})
    ;

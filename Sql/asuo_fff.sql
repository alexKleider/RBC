/* Sql/asuo_fff.sql  Applicant Satus update open
-- creates (opens) a new entry  -format x3
Uses no prefix, should changet to P_personID
and A_statusID  Also consider {status2open}     */

INSERT INTO Person_Status
        (personID, statusID, begin)
VALUES ({personID}, {status2open}, {date})
    ;

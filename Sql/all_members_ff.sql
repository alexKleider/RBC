/*  File: Sql/all_members_ff.sql
*/


SELECT P.personID, P.last, P.first, P.email FROM Person_Status
WHERE statusID in (11, 15, 14,16,17)
/* 1st yr, in good standing, honorary, inactive, retiring */
and (begin = "" OR begin <= "today")
and (end = "" OR end > "today")
;


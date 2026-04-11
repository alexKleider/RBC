/*  File: Sql/all_members_ff.sql
*/


SELECT count(*) FROM Person_Status
WHERE statusID in (11, 15, 14,16,17)
/* 1st yr, in good standing, honorary, inactive, retiring */
and (begin = "" OR begin <= "20260304")
and (end = "" OR end > "20260404")
;


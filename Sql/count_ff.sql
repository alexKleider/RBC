/*  File: Sql/count_ff.sql
*/


SELECT count(*) FROM Person_Status
WHERE statusID in (11, 15)
and (begin = "" OR begin <= "20260304")
and (end = "" OR end > "20260404")
;


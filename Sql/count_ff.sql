/*  File: Sql/count_f.sql
*/


SELECT count(*) FROM Person_Status
WHERE statusID in (11, 15)
and (begin = "" OR begin <= "{today}")
and (end = "" OR end > "{today}")
;


/*  File: Sql/n_applicants_ff.sql
  Returns the current number of applicants.
*/


SELECT count(*) FROM Person_Status
WHERE statusID < 10
and (begin = "" OR begin <= "{today}")
and (end = "" OR end > "{today}")
;


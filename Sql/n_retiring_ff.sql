/*  File: Sql/n_retiring_ff.sql
Returns number of members who have announced their
*/

SELECT count(*) FROM Person_Status
WHERE statusID =17
and (begin = "" OR begin <= "{today}")
and (end = "" OR end > "{today}")
;


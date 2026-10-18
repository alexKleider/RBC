
/*  File: Sql/n_committee_ff.sql
Returns number of 
    Requires {today} to be specified twice.
    Suggest code/sql.fetch_d_query() with a dict
    containing a "today" key
*/


SELECT count(*) FROM Person_Status
WHERE statusID > 30
AND (begin = "" OR begin <= "{today}")
AND (end = "" OR end > "{today}")
ORDER BY StatusID
;


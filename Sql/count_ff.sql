/*  File: Sql/count_f.sql
    Requires {today} to be specified twice.
    Suggest code/sql.fetch_d_query() with a dict
    containing a "today" key
*/


SELECT count(*) FROM Person_Status
WHERE statusID in (11, 15)
and (begin = "" OR begin <= "{today}")
and (end = "" OR end > "{today}")
;


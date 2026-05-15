/*  File: Sql/n_firt_yr_ff.sql
    n members in first year (not yet "in good standing.")
    Requires {today} to be specified twice.
    Suggest code/sql.fetch_d_query() with a dict
    containing a "today" key
*/


SELECT count(*) FROM Person_Status
WHERE statusID =11
and (begin = "" OR begin <= "{today}")
and (end = "" OR end > "{today}")
;


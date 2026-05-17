/*  File: Sql/n_in_good_standing_ff.sql
Returns current number of active members.
    Requires {today} to be specified twice.
    Suggest code/sql.fetch_d_query() with a dict
    containing a "today" key
*/


SELECT count(*) FROM Person_Status
WHERE statusID = 15
and (begin = "" OR begin <= "{today}")
and (end = "" OR end > "{today}")
;


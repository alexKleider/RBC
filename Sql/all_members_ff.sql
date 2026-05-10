/*  File: Sql/all_members_ff.sql

    Requires {today} to be a key provided by
    the dict supplied to code/sql.fetch_d_query()
-- includes honorary and inactive!!
-- use Sql/members_ff.sql for "proper members":
                -- 1st yr and in good standing.
*/

    SELECT P.personID, P.last, P.first, P.email
    FROM Person_Status
    WHERE statusID in (11, 14, 15, 16, 17)
        -- 11 = 1st yr, 
        -- 14 = honorary,
        -- 15 = in good standing,
        -- 16 = inactive,
        -- 17 = retiring */
    AND (begin = "" OR begin <= "today")
    AND (end = "" OR end > "today")
    ;


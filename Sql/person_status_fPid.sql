/* Sql/person_status_fPid.sql

    Requires {personID} to be a key provided by
    the dict supplied to code/sql.fetch_d_query()
*/

    SELECT statusID 
    FROM Person_Status
    WHERE personID = {personID}
        ;

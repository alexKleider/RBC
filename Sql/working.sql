/* File: Sql/try.sql
query = """
*/
        SELECT app.first, app.last, PS.statusID,
                  sp1.first, sp1.last,
                  sp2.first, sp2.last 
        FROM Applicants AS appln,
             People AS app,
             People AS sp1,
             People AS sp2,
             Person_Status as PS
        WHERE appln.personID = app.personID
        AND   appln.sponsor1ID = sp1.personID
        AND   appln.sponsor2ID = sp2.personID
        AND   PS.personID = appln.personID
        AND   PS.statusID < 11
        AND   PS.end = ""
        ORDER BY PS.statusID, PS.begin
        ;
--      """


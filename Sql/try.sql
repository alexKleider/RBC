/* File: Sql/try.sql */
        SELECT app.first, app.last,
                  app.personID, PS.statusID,
                  sp1.first, sp1.last, PS1.statusID,
                  sp2.first, sp2.last, PS2.statusID 
        FROM Applicants AS appln,
             People AS app,
             People AS sp1,
             People AS sp2,
             Person_Status as PS,
             Person_Status as PS1,
             Person_Status as PS2
        WHERE appln.personID = app.personID
        AND   appln.sponsor1ID = sp1.personID
        AND   appln.sponsor2ID = sp2.personID
        AND   PS.personID = appln.personID
        AND   PS.statusID < 11
        AND   PS1.personID = sp1.personID
        AND   PS1.end = ""
        AND   PS1.statusID < 20
        AND   PS2.personID = sp2.personID
        AND   PS2.end = ""
        AND   PS.end = ""
        AND   PS2.statusID < 20
        ORDER BY PS.statusID DESC, PS.begin DESC
        ;
--      """


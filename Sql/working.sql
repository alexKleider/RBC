/* File: Sql/try.sql
Returns a list of applicant dicts
as follows:
  {
    "P_first": "Katie",
    "P_last": "Geminder",
    "PS_statusID": 6,
    "S1_first": "Matthew",
    "S1_last": "Lundy",
    "S2_first": "James",
    "S2_last": "Finch"
  }
I don't think it's used by the code.
*/
        SELECT P.first, P.last, PS.statusID,
                  S1.first, S1.last,
                  S2.first, S2.last 
        FROM Applicants AS A,
             People AS P,
             People AS S1,
             People AS S2,
             Person_Status as PS
        WHERE A.personID = P.personID
        AND   A.sponsor1ID = S1.personID
        AND   A.sponsor2ID = S2.personID
        AND   PS.personID = A.personID
        AND   PS.statusID < 11
        AND   PS.end = ""
        ORDER BY PS.statusID, PS.begin
        ;
--      """


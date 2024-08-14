SELECT AVG(g.Grade) AS AverageGrade
FROM Grades g
JOIN Subjects sub ON g.SubjectID = sub.SubjectID
JOIN Students s ON g.StudentID = s.StudentID
JOIN Teachers t ON sub.TeacherID = t.TeacherID
WHERE s.StudentID = 1 AND t.TeacherID = 2

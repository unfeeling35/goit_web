SELECT AVG(Grade) AS AverageGrade
FROM Grades g
JOIN Subjects sub ON g.SubjectID = sub.SubjectID
WHERE sub.TeacherID = 1

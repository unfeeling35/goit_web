SELECT s.StudentID, s.First_name, s.Last_name, AVG(g.Grade) AS AverageGrade
FROM Students s
JOIN Grades g ON s.StudentID = g.StudentID
JOIN Subjects sub ON g.SubjectID = sub.SubjectID
WHERE sub.SubjectName = %s
GROUP BY s.StudentID, s.First_name, s.Last_name
ORDER BY AverageGrade DESC
LIMIT 1
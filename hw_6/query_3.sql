SELECT gr.GroupID, AVG(g.Grade) AS AverageGrade
FROM Grades g
JOIN Students s ON g.StudentID = s.StudentID
JOIN Groups gr ON s.GroupID = gr.GroupID
JOIN Subjects sub ON g.SubjectID = sub.SubjectID
WHERE sub.SubjectName = %s
GROUP BY gr.GroupID

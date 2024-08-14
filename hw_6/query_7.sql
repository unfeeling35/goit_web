SELECT s.StudentID, s.First_name, s.Last_name, g.Grade
FROM Students s
JOIN Groups gr ON s.GroupID = gr.GroupID
JOIN Grades g ON s.StudentID = g.StudentID
JOIN Subjects sub ON g.SubjectID = sub.SubjectID
WHERE gr.GroupName = %s AND sub.SubjectName = %s
SELECT DISTINCT sub.SubjectName
FROM Students s
JOIN Groups gr ON s.GroupID = gr.GroupID
JOIN Subjects sub ON gr.GroupID = s.GroupID
WHERE s.StudentID = 1

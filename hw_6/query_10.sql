SELECT DISTINCT sub.SubjectName
FROM Students s
JOIN Groups gr ON s.GroupID = gr.GroupID
JOIN Subjects sub ON gr.GroupID = s.GroupID
JOIN Teachers t ON sub.TeacherID = t.TeacherID
WHERE s.StudentID = 1 AND t.TeacherID = 2

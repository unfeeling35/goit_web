SELECT sub.SubjectName
FROM Subjects sub
JOIN Teachers t ON sub.TeacherID = t.TeacherID
WHERE t.TeacherID=3

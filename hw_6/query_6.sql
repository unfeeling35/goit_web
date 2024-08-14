SELECT s.StudentID, s.First_name, s.Last_name
FROM Students s
JOIN Groups g ON s.GroupID = g.GroupID
WHERE g.GroupName = %s
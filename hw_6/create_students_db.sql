CREATE TABLE Groups (
    GroupID SERIAL PRIMARY KEY,
    GroupName VARCHAR(50) NOT NULL
);
CREATE TABLE Teachers (
    TeacherID SERIAL PRIMARY KEY,
    First_name VARCHAR(50) NOT NULL,
    Last_name VARCHAR(50) NOT NULL
);
CREATE TABLE Subjects (
    SubjectID SERIAL PRIMARY KEY,
    SubjectName VARCHAR(100) NOT NULL,
    TeacherID INT,
    FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
);
CREATE TABLE Students (
    StudentID SERIAL PRIMARY KEY,
    First_name VARCHAR(50) NOT NULL,
    Last_name VARCHAR(50) NOT NULL,
    GroupID INT,
    FOREIGN KEY (GroupID) REFERENCES Groups(GroupID)
);
CREATE TABLE Grades (
    GradeID SERIAL PRIMARY KEY,
    StudentID INT,
    SubjectID INT,
    Grade INTEGER CHECK (Grade >= 0 AND Grade <= 100),
    DateReceived TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
)
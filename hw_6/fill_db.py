from faker import Faker
from execute_sql import execute_sql_from_file
from main import create_connection, dsn_str
import random

Faker.seed(8888)
fake = Faker(locale="uk-UA")


# print(fake_data.name())
def drop_db(connection):
    cursor = connection.cursor()

    # Remove previous data if exists
    cursor.execute('DROP TABLE IF EXISTS Students CASCADE')
    cursor.execute('DROP TABLE IF EXISTS Groups CASCADE')
    cursor.execute('DROP TABLE IF EXISTS Grades CASCADE')
    cursor.execute('DROP TABLE IF EXISTS Subjects CASCADE')
    cursor.execute('DROP TABLE IF EXISTS Teachers CASCADE')

    connection.commit()


def create_db(connection):
    cursor = connection.cursor()

    execute_sql_from_file('create_students_db.sql', cursor)
    connection.commit()


def fill_data(connection):
    cursor = connection.cursor()
    groups_data = [(fake.random_int(), fake.job()) for _ in range(3)]

    students_data = [(fake.first_name(), fake.last_name(), random.choice(groups_data)[0]) for _ in
                     range(random.randint(30, 50))]

    teachers_data = [(fake.first_name(), fake.last_name()) for _ in range(random.randint(3, 5))]

    for group in groups_data:
        cursor.execute("INSERT INTO Groups (GroupID, GroupName) VALUES (%s, %s)", group)

    for student in students_data:
        cursor.execute("INSERT INTO Students (First_name, Last_name, GroupID) VALUES (%s, %s, %s)", student)

    for teacher in teachers_data:
        cursor.execute("INSERT INTO Teachers (First_name, Last_name) VALUES (%s, %s)", teacher)

    # Щоб уникнути ситуацій коли викладач не має жодного предмета генеруємо таблицю відштовхуєчись від вже існуючих
    # викладачів
    cursor.execute("SELECT TeacherID FROM teachers")
    teachersID = cursor.fetchall()
    subjects_data = []
    for teacherID in teachersID:
        # Генеруємо 1 або 2 предмета для кожного викладача
        num_subjects = random.randint(1, 2)
        for _ in range(num_subjects):
            subjects_data.append((fake.random_int(), fake.catch_phrase(), teacherID))

    for subject in subjects_data:
        cursor.execute("INSERT INTO Subjects (SubjectID, SubjectName, TeacherID) VALUES (%s, %s, %s)", subject)

    connection.commit()


def generate_grades(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT StudentID FROM Students")
    students = cursor.fetchall()

    cursor.execute("SELECT SubjectID FROM Subjects")
    subjects = cursor.fetchall()

    # Генеруємо оцінки для кожного студента по кожному предмету
    for student in students:
        for subject in subjects:
            grade = random.randint(60, 100)
            cursor.execute("INSERT INTO Grades (StudentID, SubjectID, Grade) VALUES (%s, %s, %s)",
                           (student[0], subject[0], grade))

    connection.commit()


if __name__ == "__main__":
    with create_connection(dsn_str) as conn:
        drop_db(conn)
        create_db(conn)
        fill_data(conn)
        generate_grades(conn)

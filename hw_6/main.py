from contextlib import contextmanager
from pprint import pp as print
from dotenv import load_dotenv
import psycopg2
import sqlite3
import os

from execute_sql import execute_sql_from_file

load_dotenv()

pg_pass = os.getenv("POSTGRES_PASS")
pg_host = os.getenv("POSTGRES_HOST")

dsn_str = f"host={pg_host} dbname=postgres user=postgres password={pg_pass}"


@contextmanager
def create_connection(db_file, is_postgres=True):
    """ create a database connection to a Postgres or SQLite database """
    if is_postgres:
        conn = psycopg2.connect(dsn_str)
    else:
        conn = sqlite3.connect(db_file)
    yield conn
    conn.rollback()
    conn.close()


if __name__ == '__main__':
    with create_connection(dsn_str) as conn:
        cursor = conn.cursor()

        print('Output of query 1:')
        execute_sql_from_file('query_1.sql', cursor)
        print(cursor.fetchall())

        print('Output of query 2:')
        cursor.execute("SELECT SubjectName FROM subjects")
        subject = cursor.fetchone()
        print("Найкращий студент з предмету {}:".format(*subject))
        execute_sql_from_file('query_2.sql', cursor, *subject)
        print(cursor.fetchone())

        print('Output of query 3:')
        print("Середній бал по групах з предмету {}:".format(*subject))
        execute_sql_from_file('query_3.sql', cursor, *subject)
        print(cursor.fetchall())

        print('Output of query 4:')
        print("Середній бал на потоці")
        execute_sql_from_file('query_4.sql', cursor)
        print(cursor.fetchone())

        print('Output of query 5:')
        print("Курси певного викладача (ID=3)")
        execute_sql_from_file('query_5.sql', cursor)
        print(cursor.fetchall())

        print('Output of query 6:')
        cursor.execute("SELECT GroupName FROM groups")
        group = cursor.fetchone()
        print("Список студентів у групі {}:".format(*group))
        execute_sql_from_file('query_6.sql', cursor, *group)
        print(cursor.fetchall())

        print('Output of query 7:')
        print("Оцінки студентів у {} групі з {} предмета:".format(*group, *subject))
        execute_sql_from_file('query_7.sql', cursor, *group, *subject)
        print(cursor.fetchall())

        print('Output of query 8:')
        print("Середній бал викладача (ID=1)")
        execute_sql_from_file('query_8.sql', cursor)
        print(cursor.fetchall())

        print('Output of query 9:')
        print("Список курсів, які відвідує студент (ID=1)")
        execute_sql_from_file('query_9.sql', cursor)
        print(cursor.fetchall())

        print('Output of query 10:')
        print("Список курсів, які певному студенту читає певний викладач")
        execute_sql_from_file('query_10.sql', cursor)
        print(cursor.fetchall())

        print('Output of query 11:')
        print("Середній бал, який певний викладач ставить певному студентові")
        execute_sql_from_file('query_11.sql', cursor)
        print(cursor.fetchone())
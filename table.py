import typing
import sqlite3
import logging

column_name = str
column_type = str

class Table:
    conn: sqlite3.Connection = None

    def __init__(
        self,
        table_name: str,
        columns: dict[column_name, column_type],
        constrains: list[str],
    ) -> None:
        self.columns = columns
        self.table_name = table_name
        self.constrains = constrains

        full_columns = [f"{key} {val}" for key, val in self.columns.items()]
        full_columns.extend(constrains)

        temp = ", ".join(full_columns)

        sql_request = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({temp})"

        logging.debug(sql_request)

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_request)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.debug(e)
        finally:
            cursor.close()
        
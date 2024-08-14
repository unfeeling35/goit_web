def execute_sql_from_file(file_path, cursor, *args):
    with open(file_path, 'r') as sql_file:
        sql_queries = sql_file.read().split(';')
        for query in sql_queries:
            cursor.execute(query, args)

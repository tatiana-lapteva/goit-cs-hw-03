from psycopg2 import connect, DatabaseError, sql
from contextlib import contextmanager
from configparser import ConfigParser



def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        return {param[0]: param[1] for param in parser.items(section)}
    else:
        raise Exception(f'Section {section} not found in the {filename}')


@contextmanager
def get_connection():
    db_config = load_config()
    connection = None 
    try:
        connection = connect(**db_config)
        yield connection
        connection.commit()
    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if connection:
            connection.close()

 
def execute_query(connection, query, params=None, fetch=False):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
        except (Exception, DatabaseError) as error:
            print(f"Error: {error}")
            connection.rollback()


def drop_tables(connection, tables):
    with connection.cursor() as cursor:
        for table in tables:
            drop_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table))
            cursor.execute(drop_query)
        connection.commit()


def close_connection(connection):
    try:
        if connection:
            connection.close()
    except Exception as error:
        print(f"Error closing connection: {error}")
           
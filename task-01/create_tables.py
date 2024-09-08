
"""
Завдання 1

Створіть базу даних для системи управління завданнями, використовуючи PostgreSQL. 
База даних має містити таблиці для користувачів, статусів завдань і самих завдань. 
Виконайте необхідні запити в базі даних системи управління завданнями.
"""

from psycopg2 import connect
from postgres_helper import load_config, execute_query, drop_tables, close_connection


if __name__ == "__main__":

    try:
        db_config = load_config()
        connection = connect(**db_config)

        # Drop datatables if exist
        tables = ['users', 'status', 'tasks']
        drop_tables(connection, tables)
       

        # Create datatables
        create_dt_query = """
            CREATE TABLE status (
                id SERIAL NOT NULL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            );
            CREATE TABLE users (
                id SERIAL NOT NULL PRIMARY KEY,
                fullname VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
            CREATE TABLE tasks (
                id SERIAL NOT NULL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                status_id INTEGER REFERENCES status(id) ON DELETE SET NULL,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            );
            """
                    
        execute_query(connection, create_dt_query) 
        connection.commit()
            
    except Exception as e:
            print(f"Error: {e}")
            
    finally:
         close_connection(connection)
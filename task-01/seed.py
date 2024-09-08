
from faker import Faker
from postgres_helper import get_connection, execute_query


fake = Faker()

def generate_users_data(num_users: int) -> list[tuple[str, str]]:
    return [
        (fake.name(), fake.unique.email()) for _ in range(num_users)
    ]
    
   
def generate_tasks_data(user_ids: list[int], 
                        status_ids: list[int], 
                        num_tasks: int) -> list[tuple[str, str]]:
    return [
        (
            fake.sentence(3),
            fake.paragraph(),
            fake.random_element(status_ids),
            fake.random_element(user_ids)
        ) for _ in range(num_tasks)
    ]


if __name__ == "__main__":
    
    try:
        with get_connection() as connection:

            # Populate statuses:
            statuses = [('new',), ('in progress',), ('completed',)]
            
            for status in statuses:
                execute_query(
                    connection,
                    "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                    (status[0],)
                )

        
            # Populate users:            
            users_data = generate_users_data(50)

            for record in users_data:
                execute_query(
                    connection,
                    "INSERT INTO users (fullname, email) VALUES (%s, %s)", 
                    (record[0], record[1])
                )

            user_ids = execute_query(connection, "SELECT id FROM users", fetch=True)
            status_ids = execute_query(connection, "SELECT id FROM status", fetch=True)

            tasks_data = generate_tasks_data(user_ids, status_ids, 70)

            for record in tasks_data:
                query = """
                INSERT INTO tasks (title, description, status_id, user_id)
                VALUES (%s, %s, %s, %s)
                """
                execute_query(
                    connection,
                    query,
                    (record[0], record[1], record[2], record[3])
                )


    except Exception as error:
        print(f"Error: {error}")


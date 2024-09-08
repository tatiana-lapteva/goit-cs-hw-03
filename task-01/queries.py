
from postgres_helper import get_connection, execute_query


def print_results(header, results):
    print(f"\n{header}:\n")
    if results:
        print(results)
    else:
        print("No results found")


if __name__ == "__main__":
    
    try:
        with get_connection() as connection:
            
            # 1. Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
            user_tasks = execute_query(connection, "SELECT * FROM tasks WHERE user_id = %s", (4,), fetch=True)
            print_results("1. Завдання користувача c ID 4", user_tasks)


            # 2. Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
            tasks_status_new = execute_query(
                connection,
                """SELECT * FROM tasks 
                WHERE status_id = (SELECT id FROM status WHERE name = %s)""",
                ('new',), fetch=True)
            print_results("2. Завдання зі статусом 'new'", tasks_status_new)
        

           # 3. Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
            if tasks_status_new:
                update_task_status = tasks_status_new[0][0]
                execute_query(
                    connection,
                    """UPDATE tasks 
                    SET status_id = (SELECT id FROM status WHERE name = 'in progress')
                    WHERE id = %s""", 
                    (update_task_status,))


            # 4. Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
            users_without_tasks = execute_query(
                connection,
                """SELECT * FROM users
                WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)""",
                fetch=True)
            print_results("4. Users without tasks", users_without_tasks)


            # 5. Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.
            title, description, status_name = "Some strange task", "Make a very long homework", "new"
            status_id = execute_query(
                connection,
                "SELECT id FROM status WHERE name = %s",
                (status_name,),
                fetch=True)[0][0]
            user_id = execute_query(
                connection,
                "SELECT id FROM users ORDER BY RANDOM() LIMIT 1;",
                fetch=True)[0][0]
            execute_query(
                connection,
                """INSERT INTO tasks (title, description, status_id, user_id)
                    VALUES (%s, %s, %s, %s)""",
                (title, description, status_id, user_id))


            # 6. Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.
            not_completed_tasks =  execute_query(
                connection,
                """SELECT t.id, t.title, t.description, s.name AS status_name, t.user_id
                FROM tasks t
                JOIN status s ON t.status_id = s.id
                WHERE s.name != 'completed';""",
                fetch=True)
            print_results("6. Not completed tasks", not_completed_tasks)


            # 7. Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.
            task_id = execute_query(
                connection,
                "SELECT id FROM tasks ORDER BY RANDOM() LIMIT 1;",
                fetch=True)[0][0]
            execute_query(
                connection,
                "DELETE FROM tasks WHERE id = %s;",
                (task_id,))


            # 8. Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
            email = execute_query(
                connection,
                "SELECT email FROM users ORDER BY RANDOM() LIMIT 1;",
                fetch=True)[0][0]
            
            user_by_email = execute_query(
                connection,
                "SELECT * FROM users WHERE email LIKE %s",
                (email,), fetch=True)
            print_results("8. User with required email", user_by_email)


            # 9. Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE
            user_id = execute_query(
                connection,
                "SELECT id FROM users ORDER BY RANDOM() LIMIT 1;",
                fetch=True)[0][0]
            new_fullname = "Spounge Bob"

            execute_query(
                connection,
                "UPDATE users SET fullname = %s WHERE id = %s",
                (new_fullname, user_id))


            # 10. Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
            num_tasks = execute_query(
                connection,
                """SELECT status.name, COUNT(tasks.id) AS task_count
                FROM tasks
                JOIN status ON tasks.status_id = status.id
                GROUP BY status.name""",
                fetch=True)
            print_results("10. Number of tasks", num_tasks)


            # 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. 
            # Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, 
            # чия електронна пошта містить певний домен (наприклад, '%@example.com').

            email_domain = "example.com"
            tasks_by_domain = execute_query(
                connection,
                """SELECT tasks.id, tasks.title, tasks.description, users.email
                FROM tasks
                JOIN users ON tasks.user_id = users.id
                WHERE users.email LIKE %s""",
                (f'%{email_domain}',),
                fetch=True)
            print_results("11. Tasks with required email domain", tasks_by_domain)
            

            # 12. Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.

            tasks_without_description = execute_query(
                connection,
                """SELECT id, title, description
                FROM tasks
                WHERE description IS NULL OR description = ''""",
                fetch=True)
            print_results("12. Tasks without_description", tasks_without_description)

                        
            # 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. 
            # Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.

            tasks_in_progress = execute_query(
                connection,
                """SELECT users.id, users.fullname, tasks.id, tasks.title, tasks.description, status.name
                FROM users
                INNER JOIN tasks ON users.id = tasks.user_id
                INNER JOIN status ON tasks.status_id = status.id
                WHERE status.name = %s""",
            ('in progress',), fetch=True)
            print_results("13. Users with tasks in progress", tasks_in_progress)

    
            # 14. Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY 
            # для вибору користувачів та підрахунку їхніх завдань.

            num_users_with_tasks = execute_query(
                connection,
                """SELECT users.id, users.fullname, COUNT(tasks.id) AS task_count
                FROM users
                LEFT JOIN tasks ON users.id = tasks.user_id
                GROUP BY users.id, users.fullname
                ORDER BY task_count DESC""",
                fetch=True)
            print_results("14. Users and their task counts", num_users_with_tasks)


    except Exception as error:
        print(f"Error: {error}")


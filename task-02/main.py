
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import json_util


def add_cats(db, single_post=None, multiple_posts=None):
    if single_post:
        result_one = db.cats.insert_one(single_post)
        print(f"New post ID: {result_one.inserted_id}")
    if multiple_posts:
        result_many = db.cats.insert_many(multiple_posts)
        print(f"New post IDs: {result_many.inserted_ids}")


def find_all_cats(db):
    return list(db.cats.find({}))
     
    
def find_cat_by_name(db):
    name = input("Введіть ім'я кота: ")
    return db.cats.find_one({"name": name})


def print_post(post):
    print(json.dumps(post, default=json_util.default, ensure_ascii=False, indent=4))


def update_cat_age(db):
    name = input("Введіть ім'я кота для зміни віку: ")
    new_age = int(input("Введіть новий вік кота: "))
    result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})

    if result.matched_count > 0:
        print(f"Вік кота '{name}' оновлено до {new_age}")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено")


def add_feature_to_cat(db):
    name = input("Введіть ім'я кота: ")
    new_feature = input("Введіть нову характеристику: ")
    result = db.cats.update_one(
        {"name": name},
        {"$addToSet": {"features": new_feature}}
    )

    if result.matched_count > 0:
        if result.modified_count > 0:
            print(f"Характеристика '{new_feature}' додана до кота '{name}'")
        else:
            print(f"Характеристика '{new_feature}' вже є у кота '{name}'")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено")


def delete_cat_by_name(db):
    name = input("Введіть ім'я кота для видалення: ")
    result = db.cats.delete_one({"name": name})

    if result.deleted_count > 0:
        print(f"Кіт з ім'ям '{name}' видалений")
    else:
        print(f"Кота з ім'ям '{name}' не знайдено")


def delete_all_cats(db):
    result = db.cats.delete_many({})
    print(f"Видалено {result.deleted_count} постів")




if __name__ == "__main__":

    # Connect to the server
    uri = "mongodb+srv://tlaptevak:xQA6ahwT7RwD2UFc@cluster0.x6ffa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:

        # Validate connection
        client.admin.command('ping')

        db = client.book

        # ADD posts:
        single_cat = {
                "name": "barsik",
                "age": 3,
                "features": ["ходить в капці", "дає себе гладити", "рудий"],
            }
        add_cats(db, single_post=single_cat)

        multiple_cats = [
                {
                    "name": "Lama",
                    "age": 2,
                    "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
                },
                {
                    "name": "Liza",
                    "age": 4,
                    "features": ["ходить в лоток", "дає себе гладити", "білий"],
                },
            ]
        add_cats(db, multiple_posts=multiple_cats)


        # READ posts

        # Реалізуйте функцію для виведення всіх записів із колекції.
        all_cats = find_all_cats(db)
        print_post(all_cats)

        # Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
        result = find_cat_by_name(db)
        if result:
            print_post(result)
        else:
            print("Кота з таким ім'ям не знайдено.")


        #  UPDATE posts

        # Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
        update_cat_age(db)

        # Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
        add_feature_to_cat(db)

 
        # DELETE posts

        # Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
        delete_cat_by_name(db)

        # Реалізуйте функцію для видалення всіх записів із колекції.
        delete_all_cats(db)


    except Exception as e:
        print(e)
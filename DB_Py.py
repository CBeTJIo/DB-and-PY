import psycopg2


# Функция создания таблиц
def create_db(conn):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(20) NOT NULL,
        last_name VARCHAR(20) NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phones VARCHAR(40));
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(40) NOT NULL UNIQUE,
        client_id INTEGER NOT NULL REFERENCES users(id));
    """)
    conn.commit()


# Функция добавления клиентов
def add_client(conn, first_name, last_name, email, phones=None):
    cursor.execute("""
        INSERT INTO users (first_name, last_name, email, phones)
        VALUES (%s, %s, %s,%s) RETURNING id;
        """, (first_name, last_name, email, phones))
    client_id = cursor.fetchone()[0]
    add_phone(conn, client_id, phones)
    conn.commit()


def add_phone(conn, client_id, phones):
    if phones == None:
        pass
    else:
        cursor.execute("""
        INSERT INTO phones (phone_number, client_id)
        VALUES (%s, %s);
        """, (phones, client_id))
        conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    if first_name != None:
        cursor.execute("""
            UPDATE users
            SET first_name = %s
            WHERE id = %s
        """, (first_name, client_id))

    elif last_name != None:
        cursor.execute("""
            UPDATE users
            SET last_name = %s
                WHERE id = %s
        """, (last_name, client_id))

    elif email != None:
        cursor.execute("""
            UPDATE users
            SET email = %s
                WHERE id = %s
        """, (email, client_id))

    if phones not in list_phone(conn) and phones != None:
        add_phone(conn, client_id, phones)
    conn.commit()


# Функция удаления телефона клиента
def delete_phone(conn, client_id, phone):
    cursor.execute("""
        DELETE FROM phones
        WHERE phone_number = %s AND client_id = %s;
    """, (phone, client_id))
    conn.commit()


# Функция удаления клиента
def delete_client(conn, client_id):
    cursor.execute("""
        DELETE FROM phones WHERE client_id = %s;
        DELETE FROM users WHERE id = %s;
    """, (client_id, client_id))
    conn.commit()

# Функция поиска клиента
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if first_name == None or last_name == None or email == None:
        print(f"Просьба заполнить обязательные поля (first_name, last_name и email)")

    else:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        x = 0
        for user in users:
            x += 1
            if first_name == user[1] and last_name == user[2] and email == user[3]:
                cursor.execute(f"SELECT * FROM phones WHERE client_id = {user[0]}")
                list_phones = []
                phones = cursor.fetchall()
                for search_phone in phones:
                    list_phones.append(search_phone[1])
                print(f'Информация о клиенте: id - {user[0]}, имя - {user[1]}, фамилия - {user[2]}, email - {user[3]}, телефон(ы) - {list_phones}.')
                break
            elif x == len(users):
                print(f"Клиента {first_name} {last_name} нет в базе")


# Функия для сбора списка всех телефонов в базе
def list_phone(conn):
    cursor.execute("SELECT * FROM phones")
    phones = cursor.fetchall()
    all_phones = []
    for number in phones:
        all_phones.append(number[1])
    return all_phones


# Функция для проверки данных (НЕОБЯЗАТЕЛЬНО)
def read_query(conn, query):
    cursor.execute(query)
    return cursor.fetchall()


with psycopg2.connect(database="my_work", user="postgres", password="password") as conn:
    cursor = conn.cursor()

if __name__ == "__main__":
    # Удаление таблиц
    cursor.execute("""DROP TABLE phones;""")
    cursor.execute("""DROP TABLE users;""")
    # Примеры выполнения функций
    create_db(conn)
    add_client(conn, 'Генри', 'Кавил', 'genry_kav@mail.ru', None)
    add_client(conn, 'Джеймс', 'Бонд', '007@mail.ru', '007')
    add_client(conn, 'Бос', 'Ада', 'mefisto@mail.ru', '666')
    add_phone(conn, 1, '8-999-800-10-10')
    add_phone(conn, 1, '8-999-800-10-11')
    change_client(conn, 1, None, None, 'genry_kav', '8-55555')
    delete_phone(conn, 1, '13')
    delete_client(conn, 3)
    find_client(conn, 'Генри', 'Кавил', 'genry_kav', None)
    find_client(conn, 'Джеймс', None, None, None)
    find_client(conn, None, None, None, '007')

    # Проверка данных по пользователям (НЕОБЯЗАТЕЛЬНО)
    select_users = "SELECT * FROM users"
    users = read_query(conn, select_users)
    for user in users:
        print(user)
    # Проверка данных по телефонам (НЕОБЯЗАТЕЛЬНО)
    select_phones = "SELECT * FROM phones"
    phones = read_query(conn, select_phones)
    for phone in phones:
        print(phone)

conn.close()

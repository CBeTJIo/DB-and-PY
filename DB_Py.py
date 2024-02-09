import psycopg2

# Функция создания таблиц
def create_db(conn):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(20) NOT NULL UNIQUE,
        last_name VARCHAR(20) NOT NULL UNIQUE,
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
    cursor.execute(f"""
        INSERT INTO users (first_name, last_name, email, phones)
        VALUES (%s, %s, %s,%s) RETURNING id;
        """, (first_name, last_name, email, phones))
    client_id = cursor.fetchone()[0]
    add_phone(conn, client_id, phones)
    conn.commit()

# Функция добавления телефонов для клиентов
def add_phone(conn, client_id, phones):
    cursor.execute(f"""
    INSERT INTO phones (phone_number, client_id)
    VALUES('{phones}', '{client_id}');
    """)
    conn.commit()

# Функция изменения данных по клиенту
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    cursor.execute("""
        UPDATE users
        SET first_name = %s, last_name = %s, email = %s, phones = %s
        WHERE id = %s
    """, (first_name, last_name, email, phones, client_id))

    if phones not in list_phone(conn):
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
    if first_name != None or last_name !=None or email != None:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        x = 0
        for user in users:
            x += 1
            if first_name == user[1] or last_name == user[2] or email == user[3]:
                print(f'Информация о клиенте: id - {user[0]}, имя - {user[1]}, фамилия - {user[2]}, email - {user[3]}.')
                break
            elif x == len(users):
                print(f"Клиента {first_name} {last_name} нет в базе") #ДОПИСАТЬ!!!!!

    else:
        if phone in list_phone(conn):
            cursor.execute("SELECT * FROM phones")
            phones = cursor.fetchall()
            for search_phone in phones:
                if phone == search_phone[1]:
                    id_client = search_phone[0]
                    cursor.execute("SELECT * FROM users")
                    users = cursor.fetchall()
                    for user in users:
                        if id_client == user[0]:
                            print(f'Информация о клиенте: id - {user[0]}, имя - {user[1]}, фамилия - {user[2]}, email - {user[3]}.')
        else:
            print(f"Клиента с номером телефона {phone} нет в базе")

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
    change_client(conn, 1, 'Генри', 'Кавил', 'genry_kav', '8-55555')
    delete_phone(conn, 1, '13')
    delete_client(conn, 3)
    find_client(conn, None, 'Кавил', None, None)
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

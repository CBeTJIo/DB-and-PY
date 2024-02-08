import psycopg2

def create_db(conn):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(20) NOT NULL UNIQUE,
        last_name VARCHAR(20) NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        phones VARCHAR(40));
    CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(40) NOT NULL UNIQUE,
        client_id INTEGER NOT NULL REFERENCES users(id));
    """)

def add_client(conn,first_name, last_name, email, phones=None):
    cursor.execute(f"""
    INSERT INTO users (first_name, last_name, email, phones)
    VALUES ('{first_name}', '{last_name}', '{email}', '{phones}');
    """)

def add_phone(conn, client_id, phones):
    cursor.execute(f"""
    INSERT INTO phones (phone_number, client_id)
    VALUES('{phones}', '{client_id}');
    """)

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    cursor.execute(f"""
    UPDATE users
    SET first_name = {first_name}, last_name = {last_name}, email = {email}, phones = {phones}
    WHERE id = {client_id}
    """)

def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass

def read_query(conn, query):
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


with psycopg2.connect(database="my_work", user="postgres", password="Fry12VOT") as conn:
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE phones;""")
    cursor.execute("""DROP TABLE users;""")
    create_db(conn)
    add_client(conn, 'Генри', 'Кавил', 'genry_kav@mail.ru', None)
    add_phone(conn, 1, '8-999-800-10-10')
    add_phone(conn, 1, '8-999-800-10-11')
    change_client(conn, 1, 'Генри', 'Кавил', 'genry_kav@mail.ru','8-55555')


    select_users = "SELECT * FROM users"
    users = read_query(conn, select_users)
    for user in users:
        print(user)

    select_phones = "SELECT * FROM phones"
    phones = read_query(conn, select_phones)
    for phone in phones:
        print(phone)


conn.close()

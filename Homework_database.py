import psycopg2


# Функция для создания структуры БД
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100) UNIQUE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
                phone VARCHAR(20)
            );
        """)
    conn.commit()


# Функция для добавления нового клиента
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients (first_name, last_name, email)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (first_name, last_name, email))
        client_id = cur.fetchone()[0]
        if phones:
            for phone in phones:
                cur.execute("""
                    INSERT INTO phones (client_id, phone)
                    VALUES (%s, %s);
                """, (client_id, phone))
    conn.commit()


# Функция для добавления телефона существующему клиенту
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phones (client_id, phone)
            VALUES (%s, %s);
        """, (client_id, phone))
    conn.commit()


# Функция для изменения данных клиента
def update_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute("UPDATE clients SET first_name = %s WHERE id = %s", (first_name, client_id))
        if last_name:
            cur.execute("UPDATE clients SET last_name = %s WHERE id = %s", (last_name, client_id))
        if email:
            cur.execute("UPDATE clients SET email = %s WHERE id = %s", (email, client_id))
    conn.commit()


# Функция для удаления телефона клиента
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phones WHERE client_id = %s AND phone = %s", (client_id, phone))
    conn.commit()


# Функция для удаления клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM clients WHERE id = %s", (client_id,))
    conn.commit()


# Функция для поиска клиента
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        query = """
            SELECT c.id, c.first_name, c.last_name, c.email, p.phone
            FROM clients c
            LEFT JOIN phones p ON c.id = p.client_id
            WHERE 1=1
        """
        params = []
        if first_name:
            query += " AND c.first_name = %s"
            params.append(first_name)
        if last_name:
            query += " AND c.last_name = %s"
            params.append(last_name)
        if email:
            query += " AND c.email = %s"
            params.append(email)
        if phone:
            query += " AND p.phone = %s"
            params.append(phone)

        cur.execute(query, params)
        return cur.fetchall()

def show_all_clients(conn):
    cur = conn.cursor()
    cur.execute("SELECT first_name, last_name, email FROM clients")
    clients = cur.fetchall()

    if clients:
        print("Список всех клиентов:")
        for client in clients:
            print(f"{client[0]} {client[1]}, {client[2]}")
    else:
        print("Клиенты не найдены.")


# Пример демонстрации работы функций
def demo():
    conn = psycopg2.connect(database="clients_db", user="postgres", password="1234")

    # Проверим, что есть в базе
    show_all_clients(conn)

    # Пробуем добавить нового клиента
    add_client(conn, "Ivan", "Ivanov", "ivan@example.com", ["123456789", "987654321"])

    # Снова проверим, что есть в базе после добавления
    show_all_clients(conn)

    conn.close()

demo()
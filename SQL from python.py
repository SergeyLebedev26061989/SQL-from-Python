import psycopg2

# def create_table(cursor):
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS clients(
#         id SERIAL PRIMARY KEY,
#         first_name VARCHAR(20) NOT NULL,
#         last_name VARCHAR(30) NOT NULL,
#         email VARCHAR(255) UNIQUE
#         );
#         """)
#     cursor.execute(
#         """
#         CREATE TABLE  IF NOT EXISTS phone_clients(
#         id SERIAL PRIMARY KEY,
#         number_phone INTEGER,
#         client_id INTEGER REFERENCES clients(id)
#         );
#         """)
#     conn.commit()


def delete_db(cursor):
    cursor.execute(
        """
        DROP TABLE clients, phone_clients;
        """)


def add_client(cursor, first_name, last_name, email):
    cursor.execute(
        """
        INSERT INTO clients(first_name, last_name, email)
        VALUES(%s, %s, %s) RETURNING id;
        """, (first_name, last_name, email,))
    return cur.fetchone()


def add_phone_client(cursor, client_id, number_phone):
    cursor.execute(
        """
        INSERT INTO phone_clients(client_id, number_phone)
        VALUES(%s, %s) RETURNING id;
        """, (client_id, number_phone,))
    return cur.fetchone()


def change_client(cursor, clients_id, first_name, last_name, email, number_phones):
    cursor.execute(
        """
        UPDATE clients(clients_id, first_name, last_name, email, number_phones)
        SET first_name = %s, last_name = %s, email = %s, number_phones = %s)
        WHERE clients_id = %s;
        """, (clients_id, first_name, last_name, email, number_phones,))
    cursor.execute("""
    SELECT * FROM clients WHERE client_id=%s;""", (client_id,))
    return cur.fetchone()


def delete_phone(cursor, client_id):
    cursor.execute(
        """
        DELETE FROM phone_clients
        WHERE clients_id = %s;
        """, (client_id,))
    return cur.fetchall()
    # conn.execute(
    #     """
    #     SELECT * FROM Employes_info_;
    #     """)
    # print(conn.fetchall())


def delete_client(cursor, client_id):
    cursor.execute(
        """
        DELETE FROM clients 
        WHERE client_id = %s;  
        """, (client_id,))
    cursor.execute(
        """
        SELECT * FROM clients;
        """)
    return cur.fetchall()


def find_client(cursor, first_name, last_name, email):
    cursor.execute(
        """
        SELECT clients.id, first_name, last_name, email, number_phones
        FROM clients
        JOIN phone_clients ON clients.id = phone_clients.id
        WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s;
        """, (first_name, last_name, email,))
    return cur.fetchall()


if __name__ == '__main__':
    with psycopg2.connect(database="netology_db",
                          user="postgres",
                          password="seryoga1989") as conn:
        with conn.cursor() as cur:
            # cur.execute(
            #     """
            #     DROP TABLE clients, phone_clients CASCADE;
            #
            #     """)
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(20),
                last_name VARCHAR(40),
                email VARCHAR(255) UNIQUE
                );
                """)
            cur.execute(
                """
                CREATE TABLE  IF NOT EXISTS phone_clients(
                id SERIAL PRIMARY KEY,
                number_phone INTEGER NOT NULL,
                client_id INTEGER NOT NULL REFERENCES clients(id)
                );
                """)
            conn.commit()

            cur.execute("""
                INSERT INTO clients(first_name, last_name, email)
                VALUES('Sergey', 'Lebedev', '111@mail.ru'),
                ('Joe', 'Silver', 'Joe111@gmail.com');""")

            # print('Добавлен(ы) клиент(ы)', cur.fetchone())

            cur.execute("""
                INSERT INTO phone_clients(id, number_phone)
                VALUES(36, 6656511),
                (37, 656135513),
                (37, 1165446),
                (36, 51633);""")
            conn.commit()

            # del_tab = delete_db(cur)

            client = add_client(cur, 2, 'Mike', 'Vazovski')
            print(client)

            add_num_phone = add_phone(1, 6513132131)
            print(add_num_phone)

            change_info_client = change_client(cur, 1, 'Don', 'Kall', 'uusrb@yandex.ru', 65465135131)
            print(change_info_client)

            del_num = delete_phone(cur, 6513132131)
            print(del_num)

            del_client_ = delete_client(cur, 1)
            print(del_client_)


            search_client = find_client(cur, 'Mike', 'Vazovski', 'Mike@rambler.ru')
            print(search_client)

            conn.close()

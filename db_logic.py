import sqlite3


def get_connection(filepath):
    try:
        with open(filepath, 'x') as fp:
            pass
    except:
        pass

    conn = sqlite3.connect(filepath)
    cur = conn.cursor()
    return conn, cur


def check_table(conn, cur):
    query = f"""
    CREATE TABLE IF NOT EXISTS users_info(
        login       TEXT PRIMARY KEY,
        password    TEXT
    );
    """
    cur.execute(query)
    conn.commit()


def count_users_with_such_login(login):
    conn, cur = get_connection('db.db')

    check_table(conn, cur)

    query = f"""
    SELECT COUNT(*) FROM users_info
    WHERE login = "{login}"
    """
    cur.execute(query)
    number_of_users_with_such_login = cur.fetchall()[0][0]

    return number_of_users_with_such_login


def add_user(login, password):
    conn, cur = get_connection('db.db')

    check_table(conn, cur)

    query = f"""
    INSERT INTO users_info (login, password)
    VALUES ("{login}", "{password}")
    """
    cur.execute(query)
    conn.commit()


def get_password_by_login(login):
    conn, cur = get_connection('db.db')
    check_table(conn, cur)

    query = f"""
    SELECT password FROM users_info
    WHERE login = "{login}"
    """
    cur.execute(query)
    the_password = cur.fetchall()[0][0]

    return the_password



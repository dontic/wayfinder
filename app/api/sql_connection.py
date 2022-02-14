from pathlib import Path
import sqlite3
from sqlite3 import Error


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_connection(user):
    # Path for the user's database
    database_name = user.username + '.db'
    database_path = Path.cwd() / 'database' / database_name

    # create a database connection
    conn = None
    try:
        conn = sqlite3.connect(database_path)
        return conn
    except Error as e:
        print(e)

    # Check connection
    if conn is None:
        print("ERROR! Cannot create the database connection.")

    return conn


if __name__ == '__main__':
    from app.auth.models import User
    user = User(name='Name', email='example@email.com', username='username', password=generate_password_hash('password', method='sha256'), apikey=generate_password_hash('apikey', method='sha256'))
    create_connection(user)
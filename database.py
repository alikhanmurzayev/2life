import sqlite3
import datetime

# start database's tables names
db_name = 'pregnant.db'
users_t = 'users'
report_t = 'reports'
feeling_t = 'feeling'


# end tables names

def open_db(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    return conn, cursor
def close_db(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()

def create_users_table():
    conn, cursor = open_db(db_name)
    query = f"CREATE TABLE {users_t} (id varchar, name varchar, surname varchar, age varchar, " \
            f"week varchar, smoke varchar, cig_number varchar, alcohol varchar, disease varchar)"
    try:
        cursor.execute(query)
    except:
        pass
    close_db(conn, cursor)

def create_reports_table():
    conn, cursor = open_db(db_name)
    query = f"CREATE TABLE {report_t} (id varchar, date date, chronic varchar, " \
            f"medicine varchar, bp varchar, contacts varchar)"
    try:
        cursor.execute(query)
    except:
        pass
    close_db(conn, cursor)

def create_feeling_table():
    conn, cursor = open_db(db_name)
    query = f"CREATE TABLE {feeling_t} (id varchar, date date, feeling varchar)"
    try:
        cursor.execute(query)
    except:
        pass
    close_db(conn, cursor)

def add_user(message):
    conn, cursor = open_db(db_name)
    check = f"SELECT * FROM {users_t} WHERE id='{message.chat.id}'"
    result = cursor.execute(check).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {users_t} (id) VALUES ('{message.chat.id}')"
        cursor.execute(query)
        query = f"INSERT INTO {report_t} (id) VALUES ('{message.chat.id}')"
        cursor.execute(query)
    close_db(conn, cursor)

def set_param(message, table_name, param_name):
    conn, cursor = open_db(db_name)
    chat_id = message.chat.id
    if param_name == 'date':
        text = str(datetime.datetime.now())
    else:
        text = message.text
    query = f"UPDATE {table_name} SET {param_name}='{text}' WHERE id='{chat_id}'"
    cursor.execute(query)
    close_db(conn, cursor)

def set_feeling(message):
    conn, cursor = open_db(db_name)
    dt = str(datetime.datetime.now())
    query = f"INSERT INTO {feeling_t} (id, date, feeling) VALUES ('{message.chat.id}', '{dt}', '{message.text}')"
    cursor.execute(query)
    close_db(conn, cursor)


create_users_table()
create_reports_table()
create_feeling_table()
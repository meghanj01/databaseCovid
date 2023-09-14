import sqlite3
from flask import abort

#establish db connection
def get_db_connection():
    attempts = 0
    while attempts <3:
        try :
            
            connection = sqlite3.connect('db\my_database.db')
            connection.row_factory = sqlite3.Row  # Enables row access by name
            return connection
        except sqlite3.Error as ex:
            attempts += 1
            print(f'DB connection error {ex}')
    print('Failed to establish a DB connection after 3 attempts.')
    abort('Failed to establish connection', 500)

#close the db connection 
def close_db(conn):
    if conn:
        return conn.close()
    return

# generalised function to handle the query exection, Future score  
def db_execute(db, query):
    try:
        cur = db.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result
    except Exception as ex:
        abort(f'Internal server error {ex}', 500)



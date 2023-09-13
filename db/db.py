import sqlite3
from flask import abort

def get_db_connection():
    attempts = 0
    while attempts <3:
        try :
            connection = sqlite3.connect(':memory:')
            return connection 
        except Exception as ex:
            attempts += 1
            print(f'DB connection error {ex}')
    print('Failed to establish a DB connection after 3 attempts.')
    abort('Failed to establish connection', 500)

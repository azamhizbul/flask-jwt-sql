
import sqlite3
from sqlite3 import Error

def connect():
    conn = None
    try:
        conn = sqlite3.connect('mydb.db')
    except Error as e :
        print(e)
    return conn
import sqlite3

connection = sqlite3.connect('mydb.db')

cursor = connection.cursor()

createTable = "create table user (id int, username text, password text)"
cursor.execute(createTable)
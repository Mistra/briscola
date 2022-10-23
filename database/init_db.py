import sqlite3

connection = sqlite3.connect('database/development.db')

with open('database/schema.sql', encoding="utf-8") as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()

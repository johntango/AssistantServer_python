import sqlite3
import os

# check if db exists
if os.path.exists("prompts.db"):
    os.remove("prompts.db")

# connect to db
connection = sqlite3.connect("prompts.db")

#  create db cursor
cursor = connection.cursor()

# create table
rows = cursor.execute('''
    CREATE TABLE prompts(
        topic, 
        style,
        tone,
        language,
        prompt,
        response)
''')

# verify table creation
rows = cursor.execute('SELECT * FROM sqlite_master').fetchall()
print(rows)

#CODE FOR WHAT CREATE database.db !!DATABASE ALREADY CREATE AND WORK, USE IT ONLY IF YOU DELETE DATABASE AND WANT GET BACK IT!!

import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    user TEXT,
    areact TEXT,
    messages TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS statistic(
    allmessages TEXT,
    todaymessages TEXT,
    weekmessages TEXT,
    mouthmessages TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS messages(
    message TEXT,
    answer TEXT
)
''')

conn.commit()
conn.close()

import sqlite3
conn = sqlite3.connect('book.db')

conn.execute("create table edubook(bookid varchar(10));")

conn.commit()
conn.close()
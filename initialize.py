import sqlite3
conn = sqlite3.connect("playback.db")

conn.execute('CREATE TABLE Play (Ti TEXT, Des TEXT, Li TEXT)')
conn.close()
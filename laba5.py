import sqlite3

connection = sqlite3.connect("/Users/alexmac/Desktop/SQLlite/TLE.db")
cursor = connection.cursor()

cursor.execute('INSERT INTO TLE_1 (NORAD, NAKL, DOLGOTA, EKZT, PER, ANOMALY, CHAST) VALUES(?,?,?,?,?,?,?)',
               (25682, 97.8595, 120.6240, 0.0001164, 93.1204, 19.8568, 14.63869181437990))

cursor.execute('SELECT * FROM TLE_1')

connection.commit()
connection.close()





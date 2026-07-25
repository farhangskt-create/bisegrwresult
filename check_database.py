import sqlite3

conn = sqlite3.connect("gazette.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM students")
print("Total:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(DISTINCT roll_no) FROM students")
print("Unique Roll Numbers:", cursor.fetchone()[0])

cursor.execute("""
SELECT *
FROM students
WHERE result='ABSENT'
LIMIT 10
""")

print("\nSample ABSENT records:\n")

for row in cursor.fetchall():
    print(row)

conn.close()

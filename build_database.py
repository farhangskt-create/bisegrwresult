import fitz
import sqlite3
import re
import time

PDF_FILE = "gazette.pdf"
DB_FILE = "gazette.db"

print("Opening PDF...")

doc = fitz.open(PDF_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS students")

cursor.execute("""
CREATE TABLE students(
    roll_no TEXT PRIMARY KEY,
    name TEXT,
    result TEXT
)
""")

conn.commit()

roll_pattern = re.compile(r"^\d{6}$")

total_students = 0
start = time.time()

for page_no in range(len(doc)):

    lines = [
        line.strip()
        for line in doc[page_no].get_text().splitlines()
        if line.strip()
    ]

    i = 0

    while i < len(lines):

        if roll_pattern.fullmatch(lines[i]):

            if i + 2 < len(lines):

                roll = lines[i]
                name = lines[i + 1]
                result = lines[i + 2]

                cursor.execute(
                    "INSERT OR REPLACE INTO students VALUES (?,?,?)",
                    (roll, name, result)
                )

                total_students += 1

            i += 3

        else:
            i += 1

    # Save every 100 pages
    if page_no % 100 == 0:
        conn.commit()
        print(
            f"Processed {page_no+1}/{len(doc)} pages | "
            f"Students: {total_students}"
        )

conn.commit()

elapsed = time.time() - start

print("\n===================================")
print("Finished!")
print(f"Pages processed : {len(doc)}")
print(f"Students stored : {total_students}")
print(f"Time taken      : {elapsed:.1f} seconds")
print("===================================")

conn.close()

import sqlite3
import streamlit as st

conn = sqlite3.connect("gazette.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM students")
st.write("Total students:", cursor.fetchone()[0])

cursor.execute("SELECT * FROM students LIMIT 5")
st.write(cursor.fetchall())

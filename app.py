import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="BISE Gujranwala SSC 2025",
    page_icon="🎓",
    layout="wide"
)

DB = "gazette.db"

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

conn = get_connection()

# Statistics
total = pd.read_sql_query(
    "SELECT COUNT(*) AS total FROM students",
    conn
).iloc[0]["total"]

st.title("🎓 BISE Gujranwala SSC First Annual Examination 2025")
st.caption("Unofficial Gazette Search")

col1, col2 = st.columns(2)

with col1:
    st.metric("Students in Database", f"{total:,}")

with col2:
    st.metric("Search Speed", "< 1 second")

st.divider()

search_type = st.radio(
    "Search by",
    ["Roll Number", "Student Name"],
    horizontal=True
)

query = st.text_input(
    "Enter Roll Number or Student Name"
)

if st.button("🔍 Search", use_container_width=True):

    if not query.strip():
        st.warning("Please enter a value.")

    else:

        with st.spinner("Searching database..."):

            if search_type == "Roll Number":

                df = pd.read_sql_query(
                    "SELECT roll_no,name,result FROM students WHERE roll_no=?",
                    conn,
                    params=(query,)
                )

            else:

                df = pd.read_sql_query(
                    """
                    SELECT roll_no,name,result
                    FROM students
                    WHERE name LIKE ?
                    LIMIT 100
                    """,
                    conn,
                    params=(f"%{query.upper()}%",)
                )

        if df.empty:

            st.error("No record found.")

        else:

            st.success(f"{len(df)} record(s) found")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

st.divider()

st.caption(
    "⚠️ This search tool is provided for convenience only. "
    "Please verify your result with the official BISE Gujranwala result."
)

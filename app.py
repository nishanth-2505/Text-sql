import streamlit as st
from db import get_table_schema, run_query
from llm import generate_sql, generate_human_answer
from validator import validate_sql

TABLE_NAME = "car_sales_data"

st.set_page_config(page_title="Text to SQL (Bedrock)", layout="wide")
st.title("Text → SQL")

schema_df = get_table_schema(TABLE_NAME)
allowed_columns = schema_df["column_name"].tolist()

st.subheader("Detected Table Schema")
st.dataframe(schema_df)

user_input = st.text_area("Ask a question about your database")

if st.button("Run AI Query"):

    if user_input.strip() == "":
        st.warning("Enter a question")
        st.stop()

    schema_text = "\n".join(allowed_columns)

    with st.spinner("Generating SQL using Bedrock..."):
        sql = generate_sql(schema_text, user_input)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    if sql == "NOT POSSIBLE":
        st.error("Your question cannot be answered using available columns")
        st.stop()

    if not validate_sql(sql, allowed_columns):
        st.error("Blocked unsafe SQL (invalid column used)")
        st.stop()

    try:
        result_df = run_query(sql)
        st.subheader("Database Result")
        st.dataframe(result_df)

        with st.spinner("Generating human readable answer..."):
            explanation = generate_human_answer(user_input, sql, result_df)

        st.subheader("Human Readable Answer")
        st.success(explanation)

    except Exception as e:
        st.error(f"SQL Execution Error: {e}")

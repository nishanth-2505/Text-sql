# Text-sql
This project is an AI-powered Text-to-SQL system that allows users to query a database using natural language instead of writing SQL manually. It leverages Amazon Bedrock Large Language Models (LLMs) to automatically convert user questions into SQL queries, fetch results from a database, and return the output in a human-readable forma
The system is built using Streamlit for the user interface, Amazon Bedrock for natural language processing and reasoning, and a relational database for data storage and retrieval.

This solution helps non-technical users, analysts, and developers retrieve insights from structured data easily without requiring SQL expertise.

🎯 Problem Statement

Many users struggle with writing SQL queries to extract data from databases. This creates a dependency on technical experts and slows down decision-making.

This project solves that problem by:

Allowing users to ask questions in plain English

Automatically converting text into SQL

Fetching accurate results from the database

Presenting results in a clear and understandable summary

🚀 How the System Works (Workflow)
Step 1 — User Inputs a Natural Language Question

The user types a question such as:

"Show total car sales in 2023"

Step 2 — Database Schema Is Loaded

The system retrieves the database table schema (column names, data types) so the model understands the database structure.

Step 3 — Amazon Bedrock Converts Text to SQL

The Bedrock model analyzes:

The user question

The table schema

Column names and relationships

Then it generates an optimized SQL query.

Step 4 — SQL Query Is Executed on the Database

The generated SQL query is executed on the database, retrieving matching data.

Step 5 — Query Results Are Sent Back to Bedrock

The raw database results are sent to the Bedrock model.

Step 6 — Bedrock Converts Results to Human-Readable Output

The model summarizes the output into an easy-to-understand explanation.

Step 7 — Streamlit Displays the Final Output

The final response is displayed on the Streamlit web app.

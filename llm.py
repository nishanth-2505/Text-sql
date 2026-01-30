import os
import json
from dotenv import load_dotenv
import boto3

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

def generate_sql(schema, user_input):
    prompt = f"""
You are a PostgreSQL SQL generator.

Table name: car_sales_data

Allowed columns ONLY:
{schema}

Rules (STRICT):
- Use ONLY allowed columns from the schema
- NEVER invent columns
- If impossible return: NOT POSSIBLE
- Output ONLY SQL, no extra text
- PostgreSQL syntax only

User request:
{user_input}
"""
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 250,
        "temperature": 0
    }

    response = client.invoke_model(modelId=MODEL_ID, body=json.dumps(body))
    result = json.loads(response["body"].read())
    return result["content"][0]["text"].strip()

def generate_human_answer(user_question, sql, df):
    """
    Generate a human-readable explanation of SQL query result.
    Matches the explanation to actual data, even if empty.
    """

    
    table_data = df.head(50).to_string(index=False)

    prompt = f"""
You are an expert data analyst.

User question:
{user_question}

SQL executed:
{sql}

Query result:
{table_data}

Instructions:
- Explain the result in clear, simple human language.
- If the result is empty, explain why based on the data and user query.
- Do NOT mention SQL syntax in the explanation.
- Make the explanation easy to understand for a non-technical user.
"""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.3
    }

    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"].strip()

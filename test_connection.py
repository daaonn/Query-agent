import os
from dotenv import load_dotenv
from google.cloud import bigquery
import openai

load_dotenv()

load_dotenv()
print("키 확인:", os.getenv("OPENAI_API_KEY"))

# GPT 연결 확인
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=50,
    messages=[{"role": "user", "content": "안녕"}]
)
print("GPT 연결 OK:", response.choices[0].message.content)

# BigQuery 연결 확인
bq = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))
query = f"SELECT COUNT(*) as cnt FROM `{os.getenv('GCP_PROJECT_ID')}.{os.getenv('BQ_DATASET')}.ecommerce_sample`"
result = bq.query(query).to_dataframe()
print("BigQuery 연결 OK:", result['cnt'][0], "행 확인")
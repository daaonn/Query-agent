# sql_agent.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from metadata import METADATA, TABLE_NAME
from google.cloud import bigquery
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sql(question: str) -> str:
    prompt = f"""
너는 BigQuery SQL 전문가야.
아래 테이블 정보를 반드시 참고해서 SQL을 작성해줘.

{METADATA}

규칙:
1. 테이블명은 반드시 `{TABLE_NAME}` 을 사용해
2. SQL 코드만 출력해. 설명이나 ```sql 같은 마크다운 쓰지 마
3. 존재하지 않는 컬럼이나 값은 절대 사용하지 마
4. 날짜 필터는 EXTRACT(YEAR FROM order_date) 형식 사용해

질문: {question}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response.choices[0].message.content.strip()
    return sql

def query_bq(sql: str):
    try:
        import streamlit as st
        from google.oauth2 import service_account

        # Streamlit Cloud 환경
        if hasattr(st, 'secrets') and 'GOOGLE_PRIVATE_KEY' in st.secrets:
            credentials = service_account.Credentials.from_service_account_info(
                {
                    "type": "service_account",
                    "project_id": st.secrets["GCP_PROJECT_ID"],
                    "private_key_id": st.secrets["GOOGLE_PRIVATE_KEY_ID"],
                    "private_key": st.secrets["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
                    "client_email": st.secrets["GOOGLE_CLIENT_EMAIL"],
                    "client_id": st.secrets["GOOGLE_CLIENT_ID"],
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            )
            bq = bigquery.Client(
                project=st.secrets["GCP_PROJECT_ID"],
                credentials=credentials
            )
        # 로컬 환경
        else:
            bq = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))

        df = bq.query(sql).to_dataframe()
        return df

    except Exception as e:
        print(f"BigQuery 실행 오류: {e}")
        return None

def summarize_result(question: str, df) -> str:
    try:
        prompt = f"""
사용자 질문: {question}

데이터 조회 결과 ({len(df)}행):
{df.to_string(index=False, max_rows=20)}

위 결과를 바탕으로 아래 규칙에 맞게 요약해줘.
1. 2~3문장으로 간결하게
2. 숫자는 구체적으로 언급해
3. 한국어로 작성해
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"요약 오류: {e}")
        return None


# 테스트
if __name__ == "__main__":
    question = "카테고리별 평균 결제금액 알려줘"

    # SQL 생성
    sql = generate_sql(question)
    print(f"생성된 SQL:\n{sql}\n")

    # BigQuery 실행
    df = query_bq(sql)
    if df is not None:
        print(f"결과 ({len(df)}행):")
        print(df)
        print()

        # 결과 요약
        summary = summarize_result(question, df)
        print(f"AI 요약:\n{summary}")
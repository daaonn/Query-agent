# app.py

import streamlit as st
from sql_agent import generate_sql, query_bq, summarize_result

# 페이지 설정
st.set_page_config(page_title="자연어 데이터 추출기", page_icon="🔍")

st.title("🔍 자연어 데이터 추출기")
st.caption("질문만 입력하면 BigQuery에서 데이터를 찾아드려요")

# 질문 입력
question = st.text_input(
    "질문을 입력하세요",
    placeholder="서울 여성 스킨케어 2024년 데이터 뽑아줘"
)

if st.button("실행") and question:
    with st.spinner("분석 중..."):

        # 1. SQL 생성
        sql = generate_sql(question)
        st.subheader("📝 생성된 SQL")
        st.code(sql, language="sql")

        # 2. BigQuery 실행
        df = query_bq(sql)

        
        if df is not None:
            # 결과가 비어있을 때
            if len(df) == 0 or df.isnull().values.all():
                st.warning("조회된 데이터가 없어요. 아래 값만 사용 가능해요.")
                st.write("**카테고리:** 스킨케어, 메이크업, 헤어케어, 건강기능식품, 향수")
                st.write("**지역:** 서울, 경기, 부산, 대구, 광주, 인천, 대전")
                st.write("**기간:** 2023-01-01 ~ 2024-06-30")
            else:
                st.subheader(f"📊 결과 ({len(df)}행)")
                st.dataframe(df)
                summary = summarize_result(question, df)
                st.subheader("💬 AI 요약")
                st.info(summary)
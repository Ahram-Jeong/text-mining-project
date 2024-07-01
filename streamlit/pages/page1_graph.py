import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
final_data = pd.read_csv("../../data/doc_tone_base_rate.csv")
df = pd.DataFrame(final_data)

st.title("🔎 의사록 어조에 따른 금리 예측")
with st.sidebar :
    ds = st.date_input("조회 시작일 선택", pd.to_datetime("2005-06-06"))
    de = st.date_input("조회 종료일 선택", pd.to_datetime("2017-01-13"))

# date 컬럼 값을 datetime 값으로 변환
df["date"] = pd.to_datetime(df["date"])
# date_input에 따른 결과 DataFrame 새로 생성
date_df = df[(df["date"] >= pd.Timestamp(ds)) & (df["date"] <= pd.Timestamp(de))]

# graph 1
graph1 = plt.figure(figsize = (10, 7))
plt.rc("font", family = "NanumGothic", size = 13)
plt.rcParams["axes.unicode_minus"] = False
plt.title("의사록 어조와 기준금리의 변화 추이")
ax1 = date_df.doc_tone.plot(grid = True, label = "의사록 어조")
ax2 = date_df.baserate.plot(grid = True, label = "기준금리", secondary_y = True)
ax1.set_ylim(-1.5, 0)
st.pyplot(graph1)

# 슬라이더 날짜 선택에 맞춰 DataFrame 출력
st.dataframe(date_df, use_container_width = True)

# 산점도, 추세선
graph2 = plt.figure()
plt.title("의사록 어조에 따른 기준금리 분포도")
sns.regplot(x = "doc_tone", y = "baserate", data = date_df)
plt.xlabel("의사록 어조")
plt.ylabel("기준금리")
st.pyplot(graph2)
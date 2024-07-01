import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests as req
from bs4 import BeautifulSoup as bs

# 데이터 불러오기
final_data = pd.read_csv("data/doc_tone_base_rate.csv")
df = pd.DataFrame(final_data)

st.title("의사록 어조에 따른 금리 예측")
with st.sidebar :
    ds = st.date_input("조회 시작일 선택", pd.to_datetime("2005-06-09"))
    de = st.date_input("조회 종료일 선택", pd.to_datetime("2017-01-13"))

# date 컬럼 값을 datetime 값으로 변환
df["date"] = pd.to_datetime(df["date"])
# date_input에 따른 결과 DataFrame 새로 생성
date_df = df[(df["date"] >= pd.Timestamp(ds)) & (df["date"] <= pd.Timestamp(de))]

# graph 1
graph1 = plt.figure(figsize = (10, 7))
plt.rc("font", family = "NanumGothic", size = 13)
plt.rcParams["axes.unicode_minus"] = False
st.subheader("📈의사록 어조와 기준금리의 변화 추이")
ax1 = date_df.doc_tone.plot(label = "Doc tone")
ax2 = date_df.baserate.plot(label = "Base Rate", secondary_y = True)
# 범례 표시
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc = "upper right")
# y축 limit
ax1.set_ylim(-1, 0)
st.pyplot(graph1)

# 사이드 바 날짜 선택에 맞춰 DataFrame 출력
st.dataframe(date_df, use_container_width = True)

# graph 2
# 산점도, 추세선
graph2 = plt.figure()
st.subheader("📉의사록 어조에 따른 기준금리 분포도")
sns.regplot(x = "doc_tone", y = "baserate", data = date_df)
plt.xlabel("Doc tone")
plt.ylabel("Base Rate")
st.pyplot(graph2)

# 선택 날짜 네이버 뉴스 검색
def get_news_item(url) :
    res = req.get(url)
    soup = bs(res.text, "html.parser")
    date = soup.select_one("span.media_end_head_info_datestamp_time")["data-date-time"]
    title = soup.select_one("h2#title_area").text
    media = soup.select_one("a.media_end_head_top_logo > img")["title"]
    content = soup.select_one("div.newsct_article").text.replace("\n", "")
    return (date, title, media, content)

def get_news(ds, de) :
    page = 1
    result = []
    search = "금리"
    while True :
        if page == 11 :
            break
        start = (page - 1) * 10 + 1
        url = f"https://s.search.naver.com/p/newssearch/search.naver?de={de}&ds={ds}&eid=&field=0&force_original=&is_dts=0&is_sug_officeid=0&mynews=0&news_office_checked=&nlu_query=&nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22finance%22%7D%7D%7D&nso=%26nso%3Dso%3Add%2Cp%3Afrom{ds.replace('.', '')}to{de.replace('.', '')}%2Ca%3Aall&nx_and_query=&nx_search_hlquery=&nx_search_query=&nx_sub_query=&office_category=0&office_section_code=0&office_type=0&pd=3&photo=0&query={search}&query_original=&service_area=0&sort=0&spq=0&start={start}&where=news_tab_api&nso=so:dd,p:from{ds.replace('.', '')}to{de.replace('.', '')},a:all"
        res = req.get(url)
        doc = eval(res.text.replace("\n", ""))
        for lst in doc["contents"] :
            soup = bs(lst, "html.parser")
            a_tags = soup.select("div.info_group > a")
            if len(a_tags) == 2 :
                try :
                    result.append(get_news_item(a_tags[-1]["href"]))
                except Exception as e :
                    print("오류 : ", e)
        page += 1
    return pd.DataFrame(columns = ["date", "title", "media", "content"], data = result)
st.title("네이버 뉴스")
st.write(f"{ds.strftime('%Y-%m-%d')}부터 {de.strftime('%Y-%m-%d')}까지의 [금리] 네이버 뉴스 '관련도순' 검색 결과입니다.")

if ds and de :
    df_news = get_news(ds.strftime("%Y%m%d"), de.strftime("%Y%m%d"))
    st.dataframe(df_news)
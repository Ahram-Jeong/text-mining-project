import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 불러오기
neg_stc = pd.read_csv("data/neg_ngram_min_sentences.csv")
pos_stc = pd.read_csv("data/pos_ngram_min_sentences.csv")
neg_dict = pd.read_csv("data/total_neg_dict.csv")
pos_dict = pd.read_csv("data/total_pos_dict.csv")
neg_dict = neg_dict.rename(columns={"Unnamed: 0" : "negative_word"})
pos_dict = pos_dict.rename(columns={"Unnamed: 0" : "positive_word"})
# 그래프 한글 폰트 설정
plt.rcParams["font.family"] = "NanumGothic"

st.title("📖 극성 사전 추출 결과")

# 긍정 카운트가 가장 큰 상위 10개 단어 추출
pos_word1 = pos_dict.sort_values("Up", ascending = False).head(10)
pos_word1["positive_word"] = pos_word1["positive_word"].apply(lambda x : x.split("/")[0])
# 막대 그래프 생성
pos_fig, pos_ax = plt.subplots()
pos_bars = pos_ax.bar(pos_word1["positive_word"], pos_word1["Up"], color = "blue")
for i in pos_bars :
    y_val = i.get_height()
    pos_ax.text(i.get_x() + i.get_width() / 2, y_val + 0.05, round(y_val, 2), ha = "center", va = "bottom")

st.header("🦅️금리 상승 사전")
p_dict, pos_bar = st.columns(2)
p_dict.dataframe(pos_dict) # 금리 상승 사전 DataFrame
pos_bar.pyplot(pos_fig)

st.subheader("🦅 상위 10개의 긍정 n-grams가 포함된 의사록 문장")
pos_word2 = pos_dict.sort_values("Up", ascending = False).head(10)
pos_val = pos_word2["positive_word"].unique()
select_val2 = st.selectbox("단어를 선택하세요.", pos_val)

pos_stc = pos_stc.drop("Unnamed: 0", axis = 1)
result_pos_df = pos_stc[pos_stc["Hawkish"] == select_val2]
st.dataframe(result_pos_df)

# 부정 카운트가 가장 큰 상위 10개 단어 추출
neg_word1 = neg_dict.sort_values("Down", ascending = False).head(10)
neg_word1["negative_word"] = neg_word1["negative_word"].apply(lambda x : x.split("/")[0])
# 막대 그래프 생성
neg_fig, neg_ax = plt.subplots()
neg_bars = neg_ax.bar(neg_word1["negative_word"], neg_word1["Down"], color = "orange")
for i in neg_bars :
    y_val = i.get_height()
    neg_ax.text(i.get_x() + i.get_width() / 2, y_val + 0.05, round(y_val, 2), ha = "center", va = "bottom")

st.header("🕊️금리 하락 사전")
n_dict, neg_bar = st.columns(2)
n_dict.dataframe(neg_dict) # 금리 하락 사전 DataFrame
neg_bar.pyplot(neg_fig)

st.subheader("🕊️ 상위 10개의 부정 n-grams가 포함된 의사록 문장")
neg_word2 = neg_dict.sort_values("Down", ascending = False).head(10)
neg_val = neg_word2["negative_word"].unique()
select_val = st.selectbox("단어를 선택하세요.", neg_val)

neg_stc = neg_stc.drop("Unnamed: 0", axis = 1)
result_neg_df = neg_stc[neg_stc["Dovish"] == select_val]
st.dataframe(result_neg_df)
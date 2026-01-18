import streamlit as st
import re

st.set_page_config(page_title="虎之穴代購助手", page_icon="🐯")
st.title("🐯 虎之穴價格計算器")

# 選單放在最上方
category = st.selectbox("請選擇客戶分類：", ["分類1：親友計價", "分類2：噗浪客戶", "分類3：蝦皮客戶"])

def calculate(jpy, cat):
    if cat == "分類1：親友計價":
        return round(jpy * 0.25) if jpy <= 1000 else round(jpy * 0.26)
    elif cat == "分類2：噗浪客戶":
        return round(jpy * 0.30) if jpy <= 1000 else round(jpy * 0.32)
    elif cat == "分類3：蝦皮客戶":
        return round(jpy * 0.35) if jpy <= 1000 else round(jpy * 0.38)

# 讓手動輸入變成主要輸入，自動抓取變輔助
jpy_input = st.number_input("請輸入日幣金額 (含稅)：", min_value=0, step=1, value=0)

if jpy_input > 0:
    tw_price = calculate(jpy_input, category)
    st.divider()
    st.metric(label=f"💰 {category} 台幣總額", value=f"NT$ {tw_price}")
    st.caption(f"日幣 {jpy_input} × 判定倍率 = 台幣 {tw_price}")

st.divider()
with st.expander("嘗試自動抓取價格 (實驗性功能)"):
    st.write("若因年齡牆擋住將無法顯示，請改用上方手動輸入。")
    # ... 這裡保留你原本的 URL 抓取程式碼 ...



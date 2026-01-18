import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- 網頁基本設定 ---
st.set_page_config(page_title="虎之穴代購助手", page_icon="🐯")

# --- 介面頂部：計費規則說明 ---
with st.expander("📝 檢視計費文字規則 (點擊展開)"):
    st.markdown("""
    **分類1：親友計價**
    - ≦ 1000日幣：日幣 × 0.25
    - \> 1000日幣：日幣 × 0.26

    **分類2：噗浪客戶**
    - ≦ 1000日幣：日幣 × 0.30
    - \> 1000日幣：日幣 × 0.32

    **分類3：蝦皮客戶**
    - ≦ 1000日幣：日幣 × 0.35
    - \> 1000日幣：日幣 × 0.38
    """)

st.title("🐯 虎之穴價格計算器")

# --- 計算邏輯函式 ---
def calculate(jpy, cat):
    if cat == "分類1：親友計價":
        rate = 0.25 if jpy <= 1000 else 0.26
    elif cat == "分類2：噗浪客戶":
        rate = 0.30 if jpy <= 1000 else 0.32
    elif cat == "分類3：蝦皮客戶":
        rate = 0.35 if jpy <= 1000 else 0.38
    else:
        rate = 0
    return round(jpy * rate), rate

# --- 介面輸入區 ---
url = st.text_input("🔗 貼上商品網址：", placeholder="https://ec.toranoana.jp/...")
category = st.selectbox("👤 選擇計算分類：", ["分類1：親友計價", "分類2：噗浪客戶", "分類3：蝦皮客戶"])

scraped_jpy = 0

# --- 執行自動抓取 ---
if url:
    try:
        # 模擬已滿 18 歲的 Cookie
        cookies = {'age_check': '1', 'is_adult': '1', 'ad_check': '1'}
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0



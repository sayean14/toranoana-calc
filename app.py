import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="虎穴/BOOTH代購助手", page_icon="🐯")

# --- 側邊欄：計費規則 ---
with st.sidebar:
    st.header("📝 計費規則說明")
    st.markdown("""
    **分類1：親友計價**
    - ≦ 1000：× 0.25 / > 1000：× 0.26
    **分類2：噗浪客戶**
    - ≦ 1000：× 0.30 / > 1000：× 0.32
    **分類3：蝦皮客戶**
    - ≦ 1000：× 0.35 / > 1000：× 0.38
    """)

st.title("🐯 萬用代購計算器")

# --- 計算邏輯 ---
def calculate(jpy, cat):
    if cat == "分類1：親友計價":
        rate = 0.25 if jpy <= 1000 else 0.26
    elif cat == "分類2：噗浪客戶":
        rate = 0.30 if jpy <= 1000 else 0.32
    elif cat == "分類3：蝦皮客戶":
        rate = 0.35 if jpy <= 1000 else 0.38
    else: rate = 0
    return round(jpy * rate), rate

# --- 主要操作區 ---
category = st.selectbox("👤 選擇客戶分類：", ["分類1：親友計價", "分類2：噗浪客戶", "分類3：蝦皮客戶"])
url = st.text_input("🔗 貼上商品網址：", placeholder="https://...")

# 初始化變數
scraped_jpy = 0
scraped_title = ""

if url:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"}
        cookies = {'age_check': '1', 'is_adult': '1'}
        res = requests.get(url, headers=headers, cookies=cookies, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. 嘗試抓取標題 (BOOTH 使用 h2 或 .booth-item-name, 虎穴使用 h1)
        title_tag = soup.select_one("h1") or soup.select_one(".booth-item-name") or soup.find("title")
        if title_tag:
            scraped_title = title_tag.get_text().strip().split(' - ')[0] # 去掉網站後綴
            st.info(f"偵測到商品：{scraped_title}")

        # 2. 嘗試抓取價格
        price_tag = soup.select_





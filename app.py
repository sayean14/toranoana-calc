import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="虎穴助手", page_icon="🐯", layout="centered")

# --- 側邊欄規則 ---
with st.sidebar:
    st.markdown("### 📝 計費規則\n**親友** 0.25/0.26\n**噗浪** 0.30/0.32\n**蝦皮** 0.35/0.38")

def calculate(jpy, cat):
    if cat == "分類1：親友計價": rate = 0.25 if jpy <= 1000 else 0.26
    elif cat == "分類2：噗浪客戶": rate = 0.30 if jpy <= 1000 else 0.32
    elif cat == "分類3：蝦皮客戶": rate = 0.35 if jpy <= 1000 else 0.38
    else: rate = 0
    return round(jpy * rate), rate

st.title("🐯 快速代購計算器")

# --- 第一步：貼網址與選分類 ---
category = st.selectbox("👤 客戶分類", ["分類1：親友計價", "分類2：噗浪客戶", "分類3：蝦皮客戶"])
url = st.text_input("🔗 貼上商品網址", placeholder="https://ec.toranoana.jp/...")

scraped_title = ""

if url:
    # 嘗試抓取名稱
    try:
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"}
        res = requests.get(url, headers=headers, cookies={'age_check': '1'}, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        title_tag = soup.select_one("h1") or soup.find("title")
        if title_tag:
            scraped_title = title_tag.get_text().strip().split(' - ')[0]
            st.toast(f"已抓取名稱：{scraped_title}")
    except:
        pass

    # --- 第二步：輸入區 ---
    st.divider()
    col1, col2 = st.columns([2, 1])
    with col1:
        final_title = st.text_input("📦 商品名稱", value=scraped_title)
    with col2:
        final_jpy = st.number_input("💰 日幣金額", min_value=0, step=1)

    if final_jpy > 0:
        tw_price, used_rate = calculate(final_jpy, category)
        st.success(f"**總金額：NT$ {tw_price}** (匯率 {used_rate})")
        
        reply_text = f"【代購回報】\n{final_title}\n價格：{final_jpy}円 (匯率 {used_rate})\n總計：NT$ {tw_price}"
        st.code(reply_text, language="text")

    # --- 第三步：內建網頁預覽 (解決你的煩惱) ---
    st.divider()
    st.subheader("👀 網頁快速查看")
    st.info("請直接在下方視窗看價格，看完直接填到上方數字框！")
    
    # 使用 iframe 嵌入網頁，設定高度適合手機看價格區塊
    components.iframe(url, height=500, scrolling=True)







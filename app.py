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
        price_tag = soup.select_one(".price-taxin") or soup.select_one(".price") or soup.select_one(".detail-price-main")
        if price_tag:
            scraped_jpy = int(re.sub(r'[^\d]', '', price_tag.get_text()))
            st.success(f"✅ 已偵測價格：{scraped_jpy} 円")
        else:
            st.warning("⚠️ 價格自動抓取受限（特別是虎之穴），請手動確認。")
    except:
        st.error("連線偵測失敗，請手動輸入資訊。")

st.divider()

# --- 使用者確認區 ---
# 商品名稱輸入框，如果有抓到就預填，沒抓到就空白
final_title = st.text_input("📦 商品名稱：", value=scraped_title)
# 日幣金額輸入框
final_jpy = st.number_input("💰 日幣金額 (含稅)：", min_value=0, value=scraped_jpy)

if final_jpy > 0:
    tw_price, used_rate = calculate(final_jpy, category)
    
    st.markdown(f"### 📢 計算結果")
    st.success(f"**最終金額：NT$ {tw_price}**")
    
    # --- 格式化回覆文字 ---
    # 這裡幫你把所有資訊拼好，方便你複製
    reply_text = f"【商品代購回報】\n" \
                 f"名稱：{final_title if final_title else '未輸入'}\n" \
                 f"價格：{final_jpy}円 (匯率 {used_rate})\n" \
                 f"總計：NT$ {tw_price}"
    
    st.write("📋 點擊下方按鈕複製回覆文字：")
    st.code(reply_text, language="text")






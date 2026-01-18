import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="虎之穴代購助手", page_icon="🐯")
st.title("🐯 虎之穴價格計算器")

url = st.text_input("請貼上商品網址：", placeholder="https://ec.toranoana.jp/...")
category = st.selectbox("請選擇分類：", ["分類1：親友計價", "分類2：噗浪客戶", "分類3：蝦皮客戶"])

def calculate(jpy, cat):
    if cat == "分類1：親友計價":
        return round(jpy * 0.25) if jpy <= 1000 else round(jpy * 0.26)
    elif cat == "分類2：噗浪客戶":
        return round(jpy * 0.30) if jpy <= 1000 else round(jpy * 0.32)
    elif cat == "分類3：蝦皮客戶":
        return round(jpy * 0.35) if jpy <= 1000 else round(jpy * 0.38)

if url:
    try:
        # 強化的偽裝標頭 (User-Agent)
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://ec.toranoana.jp/"
        }
        
        # 增加連線時間設定
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 虎之穴有多種價格標籤，我們一次嘗試多個可能的路徑
        price_tag = soup.select_one(".price-taxin") or \
                    soup.select_one(".detail-price-main") or \
                    soup.select_one(".price")
        
        if price_tag:
            # 移除所有非數字字符
            jpy_text = price_tag.get_text()
            jpy = int(re.sub(r'[^\d]', '', jpy_text))
            
            tw_price = calculate(jpy, category)
            st.divider()
            st.success(f"✅ 抓取成功！")
            st.metric("日幣含稅價", f"{jpy} 円")
            st.metric(f"{category} 台幣金額", f"NT$ {tw_price}")
        else:
            # 如果抓不到，顯示目前的網頁內容片段幫助偵錯
            st.error("找不到價格標籤。")
            st.info("虎之穴可能擋住了自動抓取。請看下方的「備用方案」。")
            
    except Exception as e:
        st.error(f"連線失敗：{e}")

# --- 備用方案：如果自動抓取失敗，顯示手動輸入框 ---
st.divider()
st.subheader("💡 備用方案：手動輸入價格")
manual_jpy = st.number_input("如果自動抓不到，請手動輸入日幣金額：", min_value=0, step=1)
if manual_jpy > 0:
    manual_tw = calculate(manual_jpy, category)
    st.info(f"手動計算結果 ({category})：NT$ {manual_tw}")


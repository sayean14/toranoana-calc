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
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Referer": "https://ec.toranoana.jp/"
        }
        
        with st.spinner('連線中...'):
            res = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 尋找虎之穴多種可能的價格標籤
            price_tag = soup.select_one(".price-taxin") or \
                        soup.select_one(".detail-price-main") or \
                        soup.select_one(".price")
            
            if price_tag:
                raw_text = price_tag.get_text()
                scraped_jpy = int(re.sub(r'[^\d]', '', raw_text))
                
                final_tw, used_rate = calculate(scraped_jpy, category)
                
                st.success(f"✅ 自動抓取成功！")
                st.metric("日幣原價 (含稅)", f"{scraped_jpy} 円")
                st.metric(f"{category} (匯率 {used_rate})", f"NT$ {final_tw}")
            else:
                st.warning("⚠️ 抓不到價格標籤，請改用下方手動輸入。")
    except Exception as e:
        st.error(f"連線失敗：{e}")

# --- 手動輔助區 ---
st.divider()
st.subheader("⌨️ 手動輸入/調整")
manual_jpy = st.number_input("手動修改日幣金額：", min_value=0, value=scraped_jpy if scraped_jpy > 0 else 0)

if manual_jpy > 0:
    final_tw, used_rate = calculate(manual_jpy, category)
    if scraped_jpy == 0: # 如果自動抓取失敗才顯示這個大字
        st.metric(f"💰 {category} (匯率 {used_rate})", f"NT$ {final_tw}")
    else:
        st.caption(f"手動調整後的結果：NT$ {final_tw} (匯率 {used_rate})")




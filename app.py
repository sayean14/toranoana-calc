import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="虎穴/BOOTH代購助手", page_icon="🐯")

# --- 側邊欄：計費規則 ---
with st.sidebar:
    st.header("📝 計費規則")
    st.markdown("""
    **親友 (0.25/0.26)** | **噗浪 (0.30/0.32)** | **蝦皮 (0.35/0.38)**
    - *低倍率：≦ 1000 円*
    - *高倍率：> 1000 円*
    """)

st.title("🐯 萬用代購計算器")

def calculate(jpy, cat):
    if cat == "分類1：親友計價":
        rate = 0.25 if jpy <= 1000 else 0.26
    elif cat == "分類2：噗浪客戶":
        rate = 0.30 if jpy <= 1000 else 0.32
    elif cat == "分類3：蝦皮客戶":
        rate = 0.35 if jpy <= 1000 else 0.38
    else: rate = 0
    return round(jpy * rate), rate

# --- 操作區 ---
category = st.selectbox("👤 選擇客戶分類：", ["分類1：親友計價", "分類2：噗浪客戶", "分類3：蝦皮客戶"])
url = st.text_input("🔗 貼上商品網址：", placeholder="https://...")

scraped_jpy = 0
scraped_title = ""

if url:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"}
        cookies = {'age_check': '1', 'is_adult': '1'}
        res = requests.get(url, headers=headers, cookies=cookies, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 抓取名稱 (虎穴 h1 通常抓得到)
        title_tag = soup.select_one("h1") or soup.find("title")
        if title_tag:
            scraped_title = title_tag.get_text().strip().split(' - ')[0]
            st.toast(f"已偵測到名稱：{scraped_title}") # 手機頂部小彈窗

        # 嘗試抓取價格 (BOOTH 成功率高，虎穴目前會失敗)
        price_tag = soup.select_one(".price-taxin") or soup.select_one(".price") or soup.select_one(".detail-price-main")
        if price_tag:
            scraped_jpy = int(re.sub(r'[^\d]', '', price_tag.get_text()))
            st.success(f"✅ 價格偵測成功！")
        else:
            st.info("💡 名稱已抓取，請手動補上日幣金額。")
    except:
        st.error("連線偵測失敗")

st.divider()

# --- 手動修正區 ---
# 如果有抓到名稱就填入，沒抓到就留白
final_title = st.text_input("📦 商品名稱：", value=scraped_title)
# 這裡是你唯一需要動手的地方
final_jpy = st.number_input("💰 請輸入日幣金額 (含稅)：", min_value=0, value=scraped_jpy, step=1)

if final_jpy > 0:
    tw_price, used_rate = calculate(final_jpy, category)
    
    st.markdown(f"### 📢 總金額：**NT$ {tw_price}**")
    
    # 產出回覆文字
    reply_text = f"【商品代購回報】\n" \
                 f"名稱：{final_title}\n" \
                 f"價格：{final_jpy}円 (匯率 {used_rate})\n" \
                 f"總計：NT$ {tw_price}"
    
    st.code(reply_text, language="text")
    st.caption("點擊右上角按鈕即可複製回覆文字")








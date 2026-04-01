import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面設定
st.set_page_config(page_title="BUNNY'S 船藝備考 APP", page_icon="🐰", layout="wide")

# 2. 視覺修正 (確保字體顏色是深色，不再隱形)
st.markdown("""
<style>
    /* 強制背景與字體顏色 */
    .stApp {
        background-color: #FFFDF5 !important;
    }
    h2, h3, p, span, div {
        color: #333333 !important; /* 強制所有文字為深灰色 */
    }
    
    /* 標題與倒數 */
    .app-title { 
        text-align: center; font-size: 2rem; font-weight: 900; 
        color: #2C3E50 !important; margin: 20px 0; 
    }
    .exam-countdown { 
        background-color: #FFB7C5 !important; color: white !important; 
        border-radius: 20px; padding: 15px; text-align: center; 
        font-weight: 800; margin-bottom: 20px;
    }
    
    /* 講義區塊 */
    .note-box { 
        background-color: #F8F9FA !important; border-radius: 20px; 
        padding: 25px; border-left: 10px solid #FF9A9E; 
        margin-bottom: 20px; min-height: 200px;
    }

    /* 按鈕置中樣式 */
    div.stButton > button {
        width: 100% !important; border-radius: 30px !important;
        padding: 15px !important; font-size: 1.1rem !important;
        background-color: #FFFFFF !important; 
        color: #5C3D2E !important; border: 2px solid #EEEEEE !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 統測倒數
days_left = (datetime(2026, 4, 25) - datetime.now()).days

# 4. 資料載入
SHEET_ID = "1XIZqBYkHlt2INxq_M3yt6I4iKmzdKVblgpSafcLsk4"
URL_N = f"https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?gid=1830807869&output=csv"

@st.cache_data(ttl=5)
def load_notes():
    try:
        df = pd.read_csv(URL_N)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df_notes = load_notes()

# 5. 狀態管理
if "mode" not in st.session_state: st.session_state.mode = "HOME"
if "note_page" not in st.session_state: st.session_state.note_page = 0

# 🏠 HOME
if st.session_state.mode == "HOME":
    st.markdown(f'<div class="exam-countdown">距離 2026 統測還有 {days_left} 天 🐰</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-title">BUNNY\'S 船藝備考 APP</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin: 20px 0;'><img src='https://cdn-icons-png.flaticon.com/512/2663/2663067.png' width='100'></div>", unsafe_allow_html=True)

    if not df_notes.empty:
        chapters = sorted(df_notes["章節"].dropna().unique().tolist())
        if chapters:
            st.session_state.chapter = st.selectbox("📍 選擇目前複習章節", chapters)
            if st.button("📖 進入講義複習"):
                st.session_state.mode = "STUDY"
                st.session_state.note_page = 0
                st.rerun()
        else:
            st.warning("🐰 講義內容是空的，請在試算表填入資料喔！")
    else:
        st.error("🐰 無法連線至試算表，請確認發佈網址正確。")

# 📖 STUDY
elif st.session_state.mode == "STUDY":
    n_df = df_notes[df_notes["章節"] == st.session_state.chapter].reset_index(drop=True)
    total = len(n_df)
    cur = st.session_state.note_page
    
    row = n_df.iloc[cur]
    st.write(f"頁碼：{cur + 1} / {total}")
    st.markdown(f'<div class="note-box"><h3 style="margin-top:0;">📌 {row["重點標題"]}</h3>{row["重點內容"]}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 上一頁") and cur > 0:
            st.session_state.note_page -= 1
            st.rerun()
    with col2:
        if st.button("下一頁 ➡️") and cur < total - 1:
            st.session_state.note_page += 1
            st.rerun()
    if st.button("🏠 返回首頁"): st.session_state.mode = "HOME"; st.rerun()
        

import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面設定
st.set_page_config(page_title="BUNNY'S 船藝備考 APP", page_icon="🐰", layout="wide")

# 2. 視覺 CSS (絕對置中與 24 天倒數)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background-color: #FFFDF5 !important; font-family: 'Noto Sans TC', sans-serif !important; }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { max-width: 500px; padding: 1rem !important; margin: 0 auto; }
    .exam-countdown { background: #FFB7C5; color: white; border-radius: 20px; padding: 12px; text-align: center; margin-bottom: 20px; font-weight: 700; }
    .note-box { background-color: #F2F2F2; border-radius: 20px; padding: 25px; color: #333333; line-height: 1.8; margin-bottom: 20px; font-size: 1.1rem; border-left: 10px solid #FF9A9E; min-height: 300px; }
    div.stButton > button {
        width: 100% !important; border-radius: 30px !important;
        padding: 15px !important; font-size: 1.1rem !important;
        background: white !important; border: 1px solid #EEEEEE !important;
        color: #5C3D2E !important; font-weight: 800 !important;
        display: flex !important; justify-content: center !important; align-items: center !important;
        text-align: center !important; margin-bottom: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 統測倒數
days_left = (datetime(2026, 4, 25) - datetime.now()).days

# 4. 資料載入 (增加防呆機制)
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub?output=csv"
URL_Q = f"{BASE_URL}&gid=1898620995"
URL_N = f"{BASE_URL}&gid=1830807869"

@st.cache_data(ttl=5)
def load_csv(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame() # 失敗就回傳空表

df_questions = load_csv(URL_Q)
df_notes = load_csv(URL_N)

# 5. 狀態管理
if "mode" not in st.session_state: st.session_state.mode = "HOME"
if "note_page" not in st.session_state: st.session_state.note_page = 0

# 🏠 HOME
if st.session_state.mode == "HOME":
    st.markdown(f'<div class="exam-countdown">距離 2026 統測還有 {days_left} 天 🐰</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-weight:900;">BUNNY\'S 船藝備考 APP</h2>', unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; margin: 20px 0;'><img src='https://cdn-icons-png.flaticon.com/512/2663/2663067.png' width='100'></div>", unsafe_allow_html=True)

    # 防呆：檢查是否有章節資料
    if not df_notes.empty and "章節" in df_notes.columns:
        chapters = sorted(df_notes["章節"].dropna().unique().tolist())
        if chapters:
            st.session_state.chapter = st.selectbox("📍 選擇目前複習章節", chapters)
            if st.button("📖 進入講義複習"):
                st.session_state.mode = "STUDY"
                st.session_state.note_page = 0
                st.rerun()
            if st.button("✍️ 隨機模擬測驗"):
                st.session_state.mode = "QUIZ"
                # 簡單隨機抓題邏輯
                q_pool = df_questions[df_questions["章節"] == st.session_state.chapter]
                st.session_state.quiz_pool = q_pool.sample(n=min(5, len(q_pool))).reset_index(drop=True)
                st.session_state.quiz_idx = 0
                st.rerun()
        else:
            st.warning("🐰 講義分頁目前是空的，請在 Excel 填入內容喔！")
    else:
        st.warning("🐰 正在連線試算表...如果一直沒反應，請確認試算表已發佈。")

# 📖 STUDY (翻頁模式)
elif st.session_state.mode == "STUDY":
    n_df = df_notes[df_notes["章節"] == st.session_state.chapter].reset_index(drop=True)
    if not n_df.empty:
        total = len(n_df)
        cur = st.session_state.note_page
        row = n_df.iloc[cur]
        st.write(f"頁碼：{cur + 1} / {total}")
        st.markdown(f'<div class="note-box"><div style="font-size:1.3rem; font-weight:900; margin-bottom:10px;">📌 {row["重點標題"]}</div>{row["重點內容"]}</div>', unsafe_allow_html=True)
        
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

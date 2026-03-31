import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面設定
st.set_page_config(page_title="BUNNY'S 船藝備考 APP", page_icon="🐰", layout="wide")

# 2. 絕對置中與講義區塊 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background-color: #FFFDF5 !important; font-family: 'Noto Sans TC', sans-serif !important; }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { max-width: 500px; padding: 1rem !important; margin: 0 auto; }
    
    /* 統測倒數 */
    .exam-countdown { background: #FFB7C5; color: white; border-radius: 20px; padding: 12px; text-align: center; margin-bottom: 20px; font-weight: 700; }
    
    /* 講義內容大區塊 (灰色背景) */
    .note-box { 
        background-color: #F2F2F2; border-radius: 20px; padding: 25px; 
        color: #333333; line-height: 1.8; margin-bottom: 20px; 
        font-size: 1.1rem; min-height: 350px;
        border-left: 10px solid #FF9A9E;
    }
    .note-header { font-size: 1.3rem; font-weight: 900; color: #5C3D2E; margin-bottom: 15px; }

    /* 按鈕絕對置中樣式 */
    div.stButton > button {
        width: 100% !important; border-radius: 25px !important;
        padding: 15px !important; font-size: 1.1rem !important;
        background: white !important; border: 1px solid #EEEEEE !important;
        color: #5C3D2E !important; font-weight: 800 !important;
        text-align: center !important; 
        display: flex !important; justify-content: center !important; align-items: center !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 統測倒數 (2026/04/25)
days_left = (datetime(2026, 4, 25) - datetime.now()).days

# 4. 資料載入 (精確使用截圖中的 GID)
SHEET_ID = "1XIZqBYkHlt2INxq_M3yt6I4iKmzdKVblgpSafcLsk4"
URL_Q = f"https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?gid=1898620995&output=csv"
URL_N = f"https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?gid=1830807869&output=csv"

@st.cache_data(ttl=10)
def load_csv(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

try:
    df_questions = load_csv(URL_Q)
    df_notes = load_csv(URL_N)
except:
    st.error("🐰 資料載入失敗！請確認試算表已『發佈到網路』為 CSV 格式。")
    st.stop()

# 5. Session State
if "mode" not in st.session_state: st.session_state.mode = "HOME"
if "note_page" not in st.session_state: st.session_state.note_page = 0

# 🏠 HOME：首頁
if st.session_state.mode == "HOME":
    st.markdown(f'<div class="exam-countdown">距離 2026 統測還有 {days_left} 天 🐰</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-weight:900;">BUNNY\'S 船藝備考 APP</h2>', unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin: 30px 0;'><img src='https://cdn-icons-png.flaticon.com/512/2663/2663067.png' width='100'></div>", unsafe_allow_html=True)

    chapters = sorted(df_notes["章節"].dropna().unique().tolist())
    st.session_state.chapter = st.selectbox("📍 選擇目前複習章節", chapters)

    if st.button("📖 進入講義複習"):
        st.session_state.mode = "STUDY"
        st.session_state.note_page = 0
        st.rerun()
    
    if st.button("✍️ 隨機模擬測驗"):
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_pool = df_questions[df_questions["章節"] == st.session_state.chapter].sample(n=min(5, len(df_questions))).reset_index(drop=True)
        st.session_state.quiz_idx = 0
        st.rerun()

# 📖 STUDY：講義翻頁模式
elif st.session_state.mode == "STUDY":
    n_df = df_notes[df_notes["章節"] == st.session_state.chapter].reset_index(drop=True)
    total = len(n_df)
    cur = st.session_state.note_page
    
    if total == 0:
        st.warning("這個章節目前沒有內容喔！")
        if st.button("🏠 回首頁"): st.session_state.mode = "HOME"; st.rerun()
        st.stop()

    row = n_df.iloc[cur]
    st.write(f"頁碼：{cur + 1} / {total}")
    
    st.markdown(f"""
    <div class="note-box">
        <div class="note-header">📌 {row['重點標題']}</div>
        {row['重點內容']}
    </div>
    """, unsafe_allow_html=True)
    
    if pd.notna(row['圖片連結']):
        st.image(row['圖片連結'], use_column_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 上一頁") and cur > 0:
            st.session_state.note_page -= 1
            st.rerun()
    with col2:
        if st.button("下一頁 ➡️") and cur < total - 1:
            st.session_state.note_page += 1
            st.rerun()
            
    if st.button("🏠 返回首頁"):
        st.session_state.mode = "HOME"
        st.rerun()

# ✍️ QUIZ：隨機測驗模式
elif st.session_state.mode == "QUIZ":
    # 這裡可以沿用妳之前的刷題邏輯，重點是按鈕已透過 CSS 強制置中
    st.write("測驗模式進行中...")
    if st.button("🏠 回首頁"): st.session_state.mode = "HOME"; st.rerun()

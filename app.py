import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面設定
st.set_page_config(page_title="BUNNY'S 船藝備考 APP", page_icon="🐰", layout="wide")

# 2. 絕對置中與 3D 手機 App 視覺 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background-color: #FFFDF5 !important; font-family: 'Noto Sans TC', sans-serif !important; }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { max-width: 500px; padding: 1rem !important; margin: 0 auto; }
    
    .exam-countdown { background: #FFB7C5; color: white; border-radius: 20px; padding: 12px; text-align: center; margin-bottom: 20px; font-weight: 700; }
    .note-box { background-color: #E0E0E0; border-radius: 20px; padding: 25px; color: #333333; line-height: 1.8; margin-bottom: 20px; }

    /* 強制選項與按鈕文字絕對置中 */
    div.stButton > button {
        width: 100% !important; border-radius: 25px !important;
        padding: 15px !important; font-size: 1.1rem !important;
        background: white !important; border: 1px solid #EEEEEE !important;
        color: #5C3D2E !important; font-weight: 800 !important;
        text-align: center !important; 
        display: flex !important; justify-content: center !important; align-items: center !important;
        margin-bottom: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 統測倒數
days_left = (datetime(2026, 4, 25) - datetime.now()).days

# 4. 資料載入 (智慧讀取分頁)
# 請確認妳的網址最後面有 gid 的參數
SHEET_ID = "2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu"
URL_QUESTIONS = f"https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?gid=0&output=csv"
URL_NOTES = f"https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?gid=1506509748&output=csv" # 請更換成妳 Notes 分頁的 GID

@st.cache_data(ttl=30)
def get_df(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

try:
    df_q = get_df(URL_QUESTIONS)
    df_n = get_df(URL_NOTES)
except:
    st.error("🐰 抓不到資料...請確認 Google 試算表是否已『發佈到網路』。")
    st.stop()

# 5. 狀態管理
if "mode" not in st.session_state: st.session_state.mode = "HOME"
if "note_idx" not in st.session_state: st.session_state.note_idx = 0
if "quiz_idx" not in st.session_state: st.session_state.quiz_idx = 0
if "answered" not in st.session_state: st.session_state.answered = False

# ══════════════════════════════════════════════════════════════
# 🏠 首頁
# ══════════════════════════════════════════════════════════════
if st.session_state.mode == "HOME":
    st.markdown(f'<div class="exam-countdown">距離 2026 統測還有 {days_left} 天 🐰</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;">BUNNY\'S 船藝備考 APP</h2>', unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin: 30px 0;'><img src='https://cdn-icons-png.flaticon.com/512/2663/2663067.png' width='100'></div>", unsafe_allow_html=True)

    chapters = sorted(df_n["章節"].dropna().unique().tolist())
    st.session_state.chapter = st.selectbox("📍 選擇章節", chapters)

    if st.button("📖 系統講義複習"):
        st.session_state.mode = "STUDY"
        st.session_state.note_idx = 0 # 重頭開始看講義
        st.rerun()
    if st.button("✍️ 隨機模擬測驗"):
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_pool = df_q[df_q["章節"] == st.session_state.chapter].sample(n=min(5, len(df_q)))
        st.session_state.quiz_idx = 0
        st.rerun()

# ══════════════════════════════════════════════════════════════
# 📖 模式：講義 (讀取 Notes 分頁)
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "STUDY":
    n_df = df_n[df_n["章節"] == st.session_state.chapter].reset_index(drop=True)
    row = n_df.iloc[st.session_state.note_idx]
    
    st.markdown(f"### 講義複習：{row['知識點序號']}")
    st.markdown(f'<div class="note-box">{row["講義內容 (重點整理)"]}</div>', unsafe_allow_html=True)
    
    if pd.notna(row['講義圖片']):
        st.image(row['講義圖片'])

    if st.button("我學會了想換下一個"):
        # 抓取該講義指定的 5 個題號
        ids = [int(i.strip()) for i in str(row['關卡測驗題號 (5題)']).split(',')]
        st.session_state.quiz_pool = df_q[df_q['題號'].isin(ids)].reset_index(drop=True)
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_idx = 0
        st.session_state.answered = False
        st.rerun()

# ══════════════════════════════════════════════════════════════
# ✍️ 模式：測驗 (有答案核對)
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "QUIZ":
    q_data = st.session_state.quiz_pool.iloc[st.session_state.quiz_idx]
    st.write(f"關卡測驗：{st.session_state.quiz_idx + 1} / 5")
    st.markdown(f"### {q_data['題目']}")
    
    correct = str(q_data['正確答案']).strip().upper()

    if not st.session_state.answered:
        for opt in ["A", "B", "C

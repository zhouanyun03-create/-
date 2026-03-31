import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面基本設定
st.set_page_config(page_title="BUNNY'S 船藝備考 APP", page_icon="🐰", layout="wide")

# 2. 專業 App 視覺 CSS：解決選項置中、講義區塊樣式
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFDF5 !important;
        font-family: 'Noto Sans TC', sans-serif !important;
    }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { max-width: 500px; padding: 1rem !important; margin: 0 auto; }

    /* 統測倒數看板 */
    .exam-countdown {
        background: #FFB7C5; color: white; border-radius: 20px;
        padding: 12px; text-align: center; margin-bottom: 20px; font-weight: 700;
    }

    /* 講義內容區 (灰色背景) */
    .note-box {
        background-color: #E0E0E0; border-radius: 20px; padding: 25px;
        color: #333333; line-height: 1.8; margin-bottom: 20px; font-size: 1.05rem;
    }

    /* 按鈕與選項：強制絕對置中 */
    div.stButton > button {
        width: 100% !important; border-radius: 25px !important;
        padding: 15px !important; font-size: 1.1rem !important;
        background: white !important; border: 1px solid #EEEEEE !important;
        color: #5C3D2E !important; font-weight: 800 !important;
        display: flex !important; justify-content: center !important; align-items: center !important;
        text-align: center !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        margin-bottom: 12px !important;
    }
    div.stButton > button:hover { border-color: #FFB7C5 !important; background: #FFF9FA !important; }
</style>
""", unsafe_allow_html=True)

# 3. 統測倒數 (2026/04/25)
days_left = (datetime(2026, 4, 25) - datetime.now()).days

# 4. 資料載入邏輯
# 請確保你的試算表已發佈到網路。gid=0 為第一個分頁，gid=XXXX 為指定分頁
SHEET_ID = "2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu"
URL_Q = f"https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?gid=0&output=csv"
URL_N = f"https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?gid=1506509748&output=csv"

@st.cache_data(ttl=30)
def load_csv(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

try:
    df_questions = load_csv(URL_Q)
    df_notes = load_csv(URL_N)
except:
    st.error("🐰 資料載入失敗，請檢查試算表 GID 是否正確且已發佈。")
    st.stop()

# 5. Session State 狀態管理
if "mode" not in st.session_state: st.session_state.mode = "HOME"
if "quiz_idx" not in st.session_state: st.session_state.quiz_idx = 0
if "answered" not in st.session_state: st.session_state.answered = False

# 🏠 首頁
if st.session_state.mode == "HOME":
    st.markdown(f'<div class="exam-countdown">距離 2026 統測還有 {days_left} 天 🐰</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-weight:900;">BUNNY\'S 船藝備考 APP</h2>', unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin: 30px 0;'><img src='https://cdn-icons-png.flaticon.com/512/2663/2663067.png' width='100'></div>", unsafe_allow_html=True)

    chapters = sorted(df_notes["章節"].dropna().unique().tolist())
    st.session_state.chapter = st.selectbox("📍 選擇目前學習章節", chapters)

    if st.button("📖 系統講義複習"):
        st.session_state.mode = "STUDY"
        st.session_state.note_idx = 0
        st.rerun()
    if st.button("✍️ 隨機模擬測驗"):
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_pool = df_questions[df_questions["章節"] == st.session_state.chapter].sample(n=min(5, len(df_questions))).reset_index(drop=True)
        st.session_state.quiz_idx = 0
        st.session_state.answered = False
        st.rerun()

# 📖 模式：讀取 Notes 分頁
elif st.session_state.mode == "STUDY":
    n_df = df_notes[df_notes["章節"] == st.session_state.chapter].reset_index(drop=True)
    row = n_df.iloc[st.session_state.note_idx]
    
    st.markdown(f"### 講義重點：{row['知識點序號']}")
    st.markdown(f'<div class="note-box">{row["講義內容 (重點整理)"]}</div>', unsafe_allow_html=True)
    
    if pd.notna(row['講義圖片']):
        st.image(row['講義圖片'])

    if st.button("我學會了想換下一個 (進入測驗) ➔"):
        # 根據 Notes 中的「關卡測驗題號」欄位抓取題目
        target_ids = [int(i.strip()) for i in str(row['關卡測驗題號 (5題)']).split(',')]
        st.session_state.quiz_pool = df_questions[df_questions['題號'].isin(target_ids)].reset_index(drop=True)
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_idx = 0
        st.session_state.answered = False
        st.rerun()
    if st.button("⬅️ 返回首頁"): st.session_state.mode = "HOME"; st.rerun()

# ✍️ 模式：測驗 (對答案回饋)
elif st.session_state.mode == "QUIZ":
    pool = st.session_state.quiz_pool
    q_data = pool.iloc[st.session_state.quiz_idx]
    
    st.write(f"關卡測驗：{st.session_state.quiz_idx + 1} / {len(pool)}")
    st.markdown(f"### {q_data['題目']}")
    
    correct = str(q_data['正確答案']).strip().upper()

    if not st.session_state.answered:
        for opt in ["A", "B", "C", "D"]:
            if st.button(f"{opt}｜{q_data['選項'+opt]}", key=f"q_{opt}"):
                st.session_state.answered = True
                st.session_state.choice = opt
                st.rerun()
    else:
        if st.session_state.choice == correct: st.success(f"🎉 答對了！答案是 {correct}")
        else: st.error(f"❌ 答錯了！正確答案是 {correct}")
        
        st.info(f"💡 詳解：{q_data['解析']}")
        
        if st.button("繼續下一個項目 ➔"):
            if st.session_state.quiz_idx < len(pool) - 1:
                st.session_state.quiz_idx += 1
                st.session_state.answered = False
            else:
                st.success("本關卡測驗完成！")
                st.session_state.mode = "HOME"
            st.rerun()

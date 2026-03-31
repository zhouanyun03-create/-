import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面設定
st.set_page_config(page_title="BUNNY'S 船藝備考 APP", page_icon="🐰", layout="wide")

# 2. 強大 CSS：確保標題、選項按鈕文字絕對置中，並還原妳要的手機 App 感
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFDF5 !important;
        font-family: 'Noto Sans TC', sans-serif !important;
    }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { max-width: 500px; padding: 1.5rem !important; margin: 0 auto; }

    /* 統測倒數 */
    .exam-countdown {
        background: #FFB7C5; color: white; border-radius: 20px;
        padding: 12px; text-align: center; margin-bottom: 20px; font-weight: 700;
    }

    /* 講義內容區 (灰色背景) */
    .note-box {
        background-color: #E0E0E0; border-radius: 20px; padding: 25px;
        color: #333333; line-height: 1.8; margin-bottom: 20px; font-size: 1.05rem;
    }

    /* 按鈕絕對置中與樣式 */
    div.stButton > button {
        width: 100% !important; border-radius: 25px !important;
        padding: 15px !important; font-size: 1.1rem !important;
        background: white !important; border: 1px solid #EEEEEE !important;
        color: #5C3D2E !important; font-weight: 800 !important;
        text-align: center !important; 
        display: flex !important; justify-content: center !important; align-items: center !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        margin-bottom: 12px !important;
    }
    div.stButton > button:hover { border-color: #FFB7C5 !important; background: #FFF9FA !important; }
</style>
""", unsafe_allow_html=True)

# 3. 統測倒數 (靜態顯示)
days_left = (datetime(2026, 4, 25) - datetime.now()).days

# 4. 資料載入 (智慧辨識)
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(BASE_URL)
    df.columns = df.columns.str.strip()
    return df

df_all = load_data()

# 5. 狀態管理
if "mode" not in st.session_state: st.session_state.mode = "HOME"
if "quiz_idx" not in st.session_state: st.session_state.quiz_idx = 0
if "answered" not in st.session_state: st.session_state.answered = False

# ══════════════════════════════════════════════════════════════
# 🏠 首頁封面
# ══════════════════════════════════════════════════════════════
if st.session_state.mode == "HOME":
    st.markdown(f'<div class="exam-countdown">距離 2026 統測還有 {days_left} 天 🐰</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-weight:900;">BUNNY\'S 船藝備考 APP</h2>', unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin: 30px 0;'><img src='https://cdn-icons-png.flaticon.com/512/2663/2663067.png' width='120'></div>", unsafe_allow_html=True)

    chapters = sorted(df_all["章節"].dropna().unique().tolist())
    st.session_state.chapter = st.selectbox("📍 選擇目前學習章節", chapters)

    if st.button("📖 系統講義複習"):
        st.session_state.mode = "STUDY"
        st.rerun()
    if st.button("✍️ 隨機模擬測驗"):
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_pool = df_all[df_all["章節"] == st.session_state.chapter].sample(n=min(5, len(df_all))).reset_index(drop=True)
        st.session_state.quiz_idx = 0
        st.rerun()

# ══════════════════════════════════════════════════════════════
# 📖 模式：講義複習
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "STUDY":
    st.markdown(f"### 📖 {st.session_state.chapter} 講義重點")
    
    # 這裡會讀取妳整理後的「解析」欄位作為重點
    row = df_all[df_all["章節"] == st.session_state.chapter].iloc[0] 
    
    st.markdown(f'<div class="note-box"><b>重點整理：</b><br><br>{row["解析"]}</div>', unsafe_allow_html=True)
    
    if st.button("我學會了想換下一個 (開始測驗) ➔"):
        st.session_state.mode = "QUIZ"
        # 這裡會隨機抓 5 題跟該章節相關的題目
        st.session_state.quiz_pool = df_all[df_all["章節"] == st.session_state.chapter].sample(n=min(5, len(df_all))).reset_index(drop=True)
        st.session_state.quiz_idx = 0
        st.rerun()
    if st.button("⬅️ 返回首頁"): st.session_state.mode = "HOME"; st.rerun()

# ══════════════════════════════════════════════════════════════
# ✍️ 模式：測驗 (有對答案邏輯)
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "QUIZ":
    q_idx = st.session_state.quiz_idx
    q_data = st.session_state.quiz_pool.iloc[q_idx]
    
    st.write(f"題目 {q_idx + 1} / 5")
    st.markdown(f"### {q_data['題目']}")
    
    correct = str(q_data['正確答案']).strip().upper()

    if not st.session_state.answered:
        for opt in ["A", "B", "C", "D"]:
            if st.button(f"{opt}｜{q_data['選項'+opt]}", key=f"q_{q_idx}_{opt}"):
                st.session_state.answered = True
                st.session_state.choice = opt
                st.rerun()
    else:
        # 顯示答案回饋
        if st.session_state.choice == correct:
            st.success(f"🎉 答對了！答案是 {correct}")
        else:
            st.error(f"❌ 答錯了！正確答案是 {correct}")
        
        st.info(f"💡 詳解：{q_data['解析']}")
        
        if st.button("繼續下一題 ➔" if q_idx < 4 else "完成挑戰"):
            if q_idx < 4:
                st.session_state.quiz_idx += 1
                st.session_state.answered = False
            else:
                st.session_state.mode = "HOME"
                st.session_state.answered = False
            st.rerun()

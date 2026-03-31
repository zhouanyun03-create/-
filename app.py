import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面設定
st.set_page_config(page_title="BUNNY'S 船藝備考 APP", page_icon="🐰", layout="wide")

# 2. 視覺修正 CSS (強調絕對置中與講義區塊)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFDF5 !important;
        font-family: 'Noto Sans TC', sans-serif !important;
    }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { max-width: 500px; padding: 1.5rem !important; margin: 0 auto; }

    /* 標題與統測倒數 */
    .app-title { text-align: center; font-size: 1.8rem; font-weight: 900; color: #5C3D2E; margin: 10px 0; }
    .exam-countdown {
        background: #FFB7C5; color: white; border-radius: 20px;
        padding: 12px; text-align: center; margin-bottom: 20px; font-weight: 700;
    }

    /* 講義內容區 (灰色區塊) */
    .note-box {
        background-color: #E0E0E0; border-radius: 20px; padding: 25px;
        color: #333333; line-height: 1.8; margin-bottom: 20px; font-size: 1.05rem;
    }

    /* 按鈕與選項：絕對置中 */
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

# 3. 統測倒數 (2026/04/25)
days_left = (datetime(2026, 4, 25) - datetime.now()).days

# 4. 資料載入 (讀取兩個不同分頁)
# 注意：請將 gid=0 換成題庫分頁，gid=XXXX 換成講義分頁
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub?output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

try:
    # 這裡目前共用同一個連結，妳之後可以改為不同分頁的發佈連結
    df_questions = load_data(BASE_URL) 
    df_notes = load_data(BASE_URL) # 假設妳講義也寫在同一個表的不同列
except:
    st.error("🐰 兔子資料搬運中，請稍候...")
    st.stop()

# 5. Session State 狀態管理
if "mode" not in st.session_state: st.session_state.mode = "HOME"
if "quiz_idx" not in st.session_state: st.session_state.quiz_idx = 0
if "answered" not in st.session_state: st.session_state.answered = False
if "score" not in st.session_state: st.session_state.score = 0

# ══════════════════════════════════════════════════════════════
# 🏠 首頁
# ══════════════════════════════════════════════════════════════
if st.session_state.mode == "HOME":
    st.markdown(f'<div class="exam-countdown">距離 2026 統測還有 {days_left} 天 🐰</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-title">BUNNY\'S 船藝備考 APP</div>', unsafe_allow_html=True)
    
    st.markdown("""<div style='text-align:center; margin-bottom:20px;'><img src='https://cdn-icons-png.flaticon.com/512/2663/2663067.png' width='120'></div>""", unsafe_allow_html=True)

    chapters = sorted(df_questions["章節"].dropna().unique().tolist())
    st.session_state.chapter = st.selectbox("📍 選擇目前學習章節", chapters)

    if st.button("📖 系統講義複習"):
        st.session_state.mode = "STUDY"
        st.rerun()
    if st.button("✍️ 隨機模擬測驗"):
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_pool = df_questions[df_questions["章節"] == st.session_state.chapter].sample(n=min(5, len(df_questions))).reset_index(drop=True)
        st.session_state.quiz_idx = 0
        st.session_state.score = 0
        st.rerun()

# ══════════════════════════════════════════════════════════════
# 📖 模式：系統講義複習 (閱讀階段)
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "STUDY":
    st.markdown(f"### 📖 {st.session_state.chapter} 講義重點")
    
    # 這裡建議妳從 Notes 分頁抓資料，目前先從同表抓示範
    note_row = df_notes[df_notes["章節"] == st.session_state.chapter].iloc[0]
    
    st.markdown(f'<div class="note-box"><b>重點筆記：</b><br><br>{note_row["解析"]}</div>', unsafe_allow_html=True)
    
    if '圖片' in note_row and pd.notna(note_row['圖片']):
        st.image(note_row['圖片'], use_column_width=True)

    if st.button("我學會了想換下一個 (開始測驗) ➔"):
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_pool = df_questions[df_questions["章節"] == st.session_state.chapter].sample(n=min(5, len(df_questions))).reset_index(drop=True)
        st.session_state.quiz_idx = 0
        st.session_state.score = 0
        st.rerun()
    if st.button("⬅️ 返回主頁"): st.session_state.mode = "HOME"; st.rerun()

# ══════════════════════════════════════════════════════════════
# ✍️ 模式：測驗階段 (包含對答案邏輯)
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "QUIZ":
    q_idx = st.session_state.quiz_idx
    pool = st.session_state.quiz_pool
    
    st.write(f"題目 {q_idx + 1} / 5")
    q_data = pool.iloc[q_idx]
    st.markdown(f"### {q_data['題目']}")
    
    correct_ans = str(q_data['正確答案']).strip().upper()

    if not st.session_state.answered:
        for opt in ["A", "B", "C", "D"]:
            if st.button(f"{opt}｜{q_data['選項'+opt]}", key=f"q_{q_idx}_{opt}"):
                st.session_state.answered = True
                st.session_state.last_user_choice = opt
                if opt == correct_ans:
                    st.session_state.score += 1
                st.rerun()
    else:
        # 顯示對答案結果
        if st.session_state.last_user_choice == correct_ans:
            st.success(f"🎉 答對了！正確答案是 {correct_ans}")
        else:
            st.error(f"❌ 答錯了！正確答案是 {correct_ans}")
        
        st.info(f"💡 詳解：{q_data['解析']}")
        
        if st.button("繼續下一題 ➔" if q_idx < 4 else "查看測驗結果"):
            if q_idx < 4:
                st.session_state.quiz_idx += 1
                st.session_state.answered = False
            else:
                st.session_state.mode = "RESULT"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# 🏁 模式：測驗結果結算
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "RESULT":
    st.markdown("<h2 style='text-align:center;'>🎯 測驗結果</h2>", unsafe_allow_html=True)
    st.balloons()
    st.write(f"妳在本輪測驗中答對了 **{st.session_state.score}** 題 (共 5 題)")
    
    if st.session_state.score >= 4:
        st.success("太厲害了！這章妳已經完全掌握了。")
    else:
        st.warning("還差一點點，建議回講義再複習一下喔！")
        
    if st.button("回到首頁"):
        st.session_state.mode = "HOME"
        st.rerun()

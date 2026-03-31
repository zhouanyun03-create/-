import streamlit as st
import pandas as pd
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. 頁面設定
st.set_page_config(page_title="BUNNY'S 船藝備考 APP", page_icon="🐰", layout="wide")

# 每秒自動刷新一次 (解決你說的陽春感，讓計時器自己跑)
st_autorefresh(interval=1000, key="datarefresh")

# 2. 專業 App 視覺 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFDF5 !important;
        font-family: 'Noto Sans TC', sans-serif !important;
    }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { max-width: 500px; padding: 1rem !important; }

    /* 統測倒數計時器 */
    .exam-countdown {
        background: linear-gradient(135deg, #FFB7C5 0%, #FF9A9E 100%);
        color: white; border-radius: 15px; padding: 15px;
        text-align: center; margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(255,183,197,0.3);
    }

    /* 圓形進度條 */
    .circle-progress {
        width: 140px; height: 140px; border-radius: 50%;
        background: white; border: 10px solid #FFB7C5;
        display: flex; flex-direction: column; justify-content: center;
        align-items: center; margin: 0 auto 20px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.05);
    }

    /* 大按鈕樣式 */
    div.stButton > button {
        width: 100%; border-radius: 25px !important;
        padding: 20px !important; font-size: 1.1rem !important;
        background: white !important; border: 2px solid #F0F0F0 !important;
        color: #5C3D2E !important; font-weight: 900 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    div.stButton > button:hover { border-color: #FFB7C5 !important; background: #FFF9FA !important; }

    /* 底部考試計時器 (刷題時顯示) */
    .footer-timer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #FFB7C5; color: white; padding: 15px;
        text-align: center; font-weight: 900; font-size: 1.4rem;
        z-index: 999; letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 統測時間計算
exam_date = datetime(2026, 4, 25, 8, 0) # 假設 8:00 開始
now = datetime.now()
delta = exam_date - now
days_left = delta.days

# 4. Session State
if "mode" not in st.session_state: st.session_state.mode = "HOME"

# ══════════════════════════════════════════════════════════════
# 🏠 HOME：BUNNY'S 專屬首頁
# ══════════════════════════════════════════════════════════════
if st.session_state.mode == "HOME":
    # 統測倒數看板
    st.markdown(f"""
    <div class="exam-countdown">
        <div style="font-size:0.9rem; opacity:0.9;">距離 2026 統測還有</div>
        <div style="font-size:2.2rem; font-weight:900;">{days_left} 天</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center; color:#5C3D2E;'>🐰 BUNNY'S 船藝備考</h2>", unsafe_allow_html=True)
    
    # 圓形進度
    st.markdown("""
    <div class="circle-progress">
        <div style="font-size:0.8rem; color:#A08060;">已掌握</div>
        <div style="font-size:1.8rem; font-weight:900; color:#FFB7C5;">85%</div>
    </div>
    """, unsafe_allow_html=True)

    # 章節選擇
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub?output=csv")
    chapters = sorted(df["章節"].dropna().unique().tolist())
    curr_ch = st.selectbox("📍 選擇章節", chapters, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📖 系統講義複習"):
        st.session_state.mode = "STUDY"
        st.rerun()
        
    if st.button("✍️ 隨機模擬測驗"):
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_start = time.time()
        st.rerun()

    # 底部靜止計時 (首頁時)
    st.markdown('<div class="footer-timer">⏳ 05:00</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ✍️ QUIZ：模擬測驗 (會自動跳秒)
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "QUIZ":
    rem = max(0, 300 - int(time.time() - st.session_state.quiz_start))
    m, s = divmod(rem, 60)
    
    st.markdown(f'<div class="footer-timer">⏳ {m:02d}:{s:02d}</div>', unsafe_allow_html=True)
    
    st.write("測驗進行中...")
    if st.button("⬅️ 放棄返回"): st.session_state.mode = "HOME"; st.rerun()
    if rem == 0: st.error("時間到！"); st.session_state.mode = "HOME"
        

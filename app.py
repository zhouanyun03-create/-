import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 頁面基本設定
st.set_page_config(page_title="BUNNY'S 船藝備考 APP", page_icon="🐰", layout="wide")

# 2. 修正後的 UI CSS (移除所有計時器相關樣式，確保選項置中)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFDF5 !important;
        font-family: 'Noto Sans TC', sans-serif !important;
        color: #444444 !important;
    }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { max-width: 500px; padding: 1rem !important; margin: 0 auto; }

    /* 統測倒數看板 (靜態顯示) */
    .exam-countdown {
        background: linear-gradient(135deg, #FFB7C5 0%, #FF9A9E 100%);
        color: white; border-radius: 20px; padding: 15px;
        text-align: center; margin-bottom: 20px;
    }

    /* 圓形進度條視覺 */
    .circle-progress {
        width: 140px; height: 140px; border-radius: 50%;
        background: white; border: 10px solid #FFB7C5;
        display: flex; flex-direction: column; justify-content: center;
        align-items: center; margin: 0 auto 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* 講義灰色重點區塊 */
    .handout-box {
        background-color: #F2F2F2; border-radius: 20px; padding: 25px;
        color: #444444; line-height: 1.8; margin-bottom: 20px;
        border-left: 10px solid #FFB7C5;
    }

    /* 選項按鈕：強制水平與垂直置中 */
    div.stButton > button {
        width: 100% !important; border-radius: 30px !important;
        padding: 15px !important; font-size: 1.1rem !important;
        background: white !important; border: 1px solid #EEEEEE !important;
        color: #5C3D2E !important; font-weight: 800 !important;
        display: block !important;
        text-align: center !important; /* 水平置中 */
        margin-bottom: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 統測倒數 (靜態計算)
days_left = (datetime(2026, 4, 25) - datetime.now()).days

# 4. 資料載入
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df_all = load_data()

# 5. 狀態管理
if "mode" not in st.session_state: st.session_state.mode = "HOME"
if "idx" not in st.session_state: st.session_state.idx = 0

# ══════════════════════════════════════════════════════════════
# 🏠 HOME：BUNNY'S 首頁
# ══════════════════════════════════════════════════════════════
if st.session_state.mode == "HOME":
    st.markdown(f'<div class="exam-countdown">距離 2026 統測還有 <b>{days_left}</b> 天 🐰</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; font-weight:900;'>🐰 BUNNY'S 船藝備考 APP</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="circle-progress"><div style="font-size:0.8rem; color:#A08060;">已掌握</div><div style="font-size:1.8rem; font-weight:900; color:#FFB7C5;">85%</div></div>', unsafe_allow_html=True)

    chapters = sorted(df_all["章節"].dropna().unique().tolist())
    st.session_state.chapter = st.selectbox("📍 選擇目前學習章節", chapters)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📖 系統講義複習"):
        st.session_state.mode = "STUDY"
        st.rerun()
    if st.button("✍️ 隨機模擬測驗"):
        st.session_state.mode = "QUIZ"
        # 隨機抓5題
        st.session_state.quiz_pool = df_all[df_all["章節"] == st.session_state.chapter].sample(n=min(5, len(df_all))).reset_index(drop=True)
        st.session_state.quiz_idx = 0
        st.rerun()

# ══════════════════════════════════════════════════════════════
# 📖 STUDY：講義模式 (顯示解析作為重點)
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "STUDY":
    st.markdown(f"### 📖 {st.session_state.chapter} 重點整理")
    # 抓取該章節第一筆解析作為示範講義
    row = df_all[df_all["章節"] == st.session_state.chapter].iloc[0]
    
    st.markdown(f'<div class="handout-box"><b>重點筆記：</b><br><br>{row["解析"]}</div>', unsafe_allow_html=True)
    
    if st.button("我讀完了，開始 5 題測驗 ➔"):
        st.session_state.mode = "QUIZ"
        st.session_state.quiz_pool = df_all[df_all["章節"] == st.session_state.chapter].sample(n=min(5, len(df_all))).reset_index(drop=True)
        st.session_state.quiz_idx = 0
        st.rerun()
    if st.button("⬅️ 返回首頁"): st.session_state.mode = "HOME"; st.rerun()

# ══════════════════════════════════════════════════════════════
# ✍️ QUIZ：測驗模式 (完全移除計時器)
# ══════════════════════════════════════════════════════════════
elif st.session_state.mode == "QUIZ":
    q_idx = st.session_state.quiz_idx
    if q_idx < len(st.session_state.quiz_pool):
        q_data = st.session_state.quiz_pool.iloc[q_idx]
        st.write(f"題目 {q_idx + 1} / 5")
        st.write(f"### {q_data['題目']}")
        
        for opt in ["A", "B", "C", "D"]:
            if st.button(f"{opt}｜{q_data['選項'+opt]}", key=f"q_{q_idx}_{opt}"):
                if q_idx + 1 < 5:
                    st.session_state.quiz_idx += 1
                else:
                    st.balloons()
                    st.success("完成本輪測驗！")
                    st.session_state.mode = "HOME"
                st.rerun()
    
    if st.button("⬅️ 中途退出"): st.session_state.mode = "HOME"; st.rerun()
        

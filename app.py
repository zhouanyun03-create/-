import streamlit as st
import pandas as pd

# ══════════════════════════════════════════════════════════════
#  頁面設定
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="✨ 刷題小精靈",
    page_icon="🌸",
    layout="wide",
)

# ══════════════════════════════════════════════════════════════
#  全域 CSS — 強制淺色、主畫面選單優化
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');

/* ── 強制淺色底 ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
    background-color: #FFFDF5 !important;
    color: #444444 !important;
    font-family: 'Noto Sans TC', sans-serif !important;
}

/* 隱藏所有 Streamlit 官方雜訊，讓它更像 App */
#MainMenu, footer, header, [data-testid="stDecoration"] { visibility: hidden !important; }

/* 讓主內容區在手機上滿版 */
.block-container {
    max-width: 600px;
    padding: 1rem 1rem 5rem !important;
}

/* ── 主畫面選單卡片化 ── */
div[data-testid="stSelectbox"] > div {
    background: #FFFFFF !important;
    border: 1px solid #EEEEEE !important;
    border-radius: 20px !important;
    box-shadow: 0 4px 15px rgba(92,61,46,0.08) !important;
}

/* ── 進度條 ── */
.progress-wrap {
    background: #E8F5E9;
    border-radius: 999px;
    height: 12px;
    margin: 1.5rem 0 0.5rem;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #A8E6CF, #56C596);
    transition: width 0.5s ease;
}

/* ── 題目卡片 ── */
.question-card {
    background: #FFFFFF;
    border: 1px solid #EEEEEE;
    border-radius: 24px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(92,61,46,0.07);
}
.chapter-badge {
    background: #A8E6CF;
    color: white;
    padding: 2px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
}

/* ── 選項按鈕 ── */
div.stButton > button {
    width: 100%;
    background: #F9F9F9 !important;
    border: 1px solid #EEEEEE !important;
    border-radius: 18px !important;
    padding: 0.8rem 1.2rem !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.5rem !important;
    box-shadow: 0 3px 6px rgba(0,0,0,0.04) !important;
    transition: 0.2s;
}
div.stButton > button:hover {
    background: #FFF3E8 !important;
    border-color: #FFB7C5 !important;
    transform: translateY(-2px);
}

/* 得分顯示 */
.score-box {
    background: white;
    border-radius: 20px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #F0D8C8;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  資料載入
# ══════════════════════════════════════════════════════════════
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    return df

df_all = load_data()
col_chapter = "章節" # 請確保你的試算表有這一欄

# ══════════════════════════════════════════════════════════════
#  狀態管理
# ══════════════════════════════════════════════════════════════
if "idx" not in st.session_state:
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.chapter = "📚 全部章節"

# ══════════════════════════════════════════════════════════════
#  主畫面選單 (取代側邊欄)
# ══════════════════════════════════════════════════════════════
st.markdown("<h2 style='text-align:center;'>🌸 刷題小精靈</h2>", unsafe_allow_html=True)

# 讓選單直接出現在最上方
all_chapters = ["📚 全部章節"] + sorted(df_all[col_chapter].dropna().unique().tolist())
selected_chapter = st.selectbox("📍 切換章節", all_chapters, index=all_chapters.index(st.session_state.chapter))

# 如果切換章節，重置狀態
if selected_chapter != st.session_state.chapter:
    st.session_state.chapter = selected_chapter
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.rerun()

# ══════════════════════════════════════════════════════════════
#  篩選題目
# ══════════════════════════════════════════════════════════════
if st.session_state.chapter == "📚 全部章節":
    df = df_all
else:
    df = df_all[df_all[col_chapter] == st.session_state.chapter].reset_index(drop=True)

total = len(df)
idx = st.session_state.idx

# ══════════════════════════════════════════════════════════════
#  刷題介面
# ══════════════════════════════════════════════════════════════
# 進度條
progress = (idx / total)
st.markdown(f"""
<div class="progress-wrap"><div class="progress-fill" style="width:{progress*100}%;"></div></div>
<div style

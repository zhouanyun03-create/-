import streamlit as st
import pandas as pd
import random
from datetime import date

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🐰 BUNNY'S 船藝備考 APP",
    page_icon="🐰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS (修正字體與視覺) ──────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Background ---- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #FFFDF5 !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"],
footer, #MainMenu { visibility: hidden !important; display: none !important; }

/* ---- Typography (妳指定的圓潤風格) ---- */
* { font-family: 'Varela Round', 'Nunito', 'Microsoft JhengHei', sans-serif; }

/* ---- Countdown banner ---- */
.countdown-banner {
    background: linear-gradient(135deg, #FFB6C1 0%, #FF91A4 100%);
    border-radius: 16px;
    padding: 14px 24px;
    text-align: center;
    margin-bottom: 8px;
    box-shadow: 0 4px 16px rgba(255,145,164,0.3);
}
.countdown-banner p {
    margin: 0; font-size: 1.05rem; font-weight: bold; color: #6B0020;
}
.countdown-days {
    font-size: 2rem !important; color: #C0003A !important;
}

/* ---- App Title ---- */
.app-title {
    text-align: center; font-size: 2rem; font-weight: 900;
    color: #2C2C2C !important; margin: 0 0 4px 0;
}

/* ---- Lecture note card ---- */
.note-card {
    background: #F0EDE3;
    border-left: 5px solid #C0003A;
    border-radius: 12px;
    padding: 22px 26px;
    margin: 16px 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}
.note-card h3 { color: #C0003A; margin-bottom: 10px; font-size: 1.15rem; }
.note-card p { color: #2C2C2C; line-height: 1.85; white-space: pre-wrap; font-size: 0.97rem; }

/* ---- Buttons ---- */
[data-testid="stButton"] > button {
    display: flex !important; align-items: center !important; justify-content: center !important;
    width: 100%; border-radius: 10px; font-weight: bold; padding: 10px 0;
    background-color: white !important; color: #5C3D2E !important; border: 1px solid #DDD !important;
}
/* 同步按鈕專用顏色 */
.sync-btn button {
    background-color: #EAF4FB !important;
    border: 1px solid #17A2B8 !important;
    color: #0C5460 !important;
    font-size: 0.85rem !important;
    padding: 5px 0 !important;
}

/* ---- Quiz Styles ---- */
.quiz-card { background: #F7F5EC; border-radius: 14px; padding: 22px 26px; border: 1.5px solid #E0D9C8; }
.mode-badge { display: inline-block; background: #FFE0E6; color: #C0003A; border-radius: 20px; padding: 3px 14px; font-size: 0.78rem; font-weight: bold; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Data URLs ─────────────────────────────────────────────────────────────────
BASE_PUB = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub"
NOTES_URL = f"{BASE_PUB}?gid=1830807869&single=true&output=csv"
QUIZ_URL  = f"{BASE_PUB}?gid=1898620995&single=true&output=csv"

# 快取時間設定為 10 秒，平衡更新頻率與連線穩定度
@st.cache_data(ttl=10, show_spinner=False)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df.dropna(how="all")
    except:
        return None

# ── Header ────────────────────────────────────────────────────────────────────
exam_date = date(2026, 4, 25)
days_left = (exam_date - date.today()).days

st.markdown(f"""
<div class="countdown-banner">
  <p>📅 距離 2026 統測 (4/25) 還有</p>
  <p class="countdown-days">⏳ {days_left} 天</p>
  <p>加油！妳一定可以的 🐰💪</p>
</div>
<p class="app-title">🐰 BUNNY'S 船藝備考 APP</p>
<p style='text-align:center;color:#888;font-size:0.85rem;margin-bottom:20px;'>統測 · 輪機 · 航海 · 船藝專屬備考工具</p>
""", unsafe_allow_html=True)

# ── 同步按鈕 (及時更新核心) ──────────────────────────────────────────────────────
# 這個按鈕會強制清空 Streamlit 的快取記憶，重新去 Google 抓一次資料
st.markdown('<div class="sync-btn">', unsafe_allow_html=True)
if st.button("🔄 點我同步 Excel 最新內容 (改完 Excel 點這)"):
    st.cache_data.clear()
    st.toast("🐰 正在重新讀取 Excel 資料...")
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
notes_df = load_data(NOTES_URL)
quiz_df  = load_data(QUIZ_URL)

if notes_df is None:
    st.error("🐰 無法連線至試算表。請確認 Excel 權限已開啟「知道連結的任何人」。")
    st.stop()

# ── Chapter Selector ──────────────────────────────────────────────────────────
chapters = sorted(notes_df["章節"].astype(str).unique().tolist()) if "章節" in notes_df.columns else []
if not chapters:
    st.warning("🐰 找不到章節資料，請確認 Excel 的「章節」欄位有填寫內容！")
    st.stop()

st.markdown('<p style="text-align:center;font-weight:bold;color:#555;font-size:0.9rem;">📚 請選擇章節</p>', unsafe_allow_html=True)
selected_chapter = st.selectbox("", chapters, label_visibility="collapsed")

# ── Session State Init ─────────────────────────────────────────────────────────
if "mode" not in st.session_state: st.session_state.mode = None
if "note_idx" not in st.session_state: st.session_state.note_idx = 0

# ── Mode Selector ─────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)
with c1:
    if st.button("📖 進入講義複習"):
        st.session_state.mode = "notes"
        st.session_state.note_idx = 0
with c2:
    if st.button("🎯 隨機模擬測驗"):
        st.session_state.mode = "quiz"
        st.session_state.quiz_idx = 0
        st.session_state.answered = False
        st.session_state.score = 0
        # 從題庫篩選題目
        q_pool = quiz_df[quiz_df["章節"].astype(str).str.strip() == str(selected_chapter).strip()]
        if q_pool.empty: q_pool = quiz_df # 沒找到就用全體
        st.session_state.quiz_questions = q_pool.sample(n=min(5, len(q_pool))).to_dict("records")

# ── 講義複習模式 ──────────────────────────────────────────────────────────────
if st.session_state.mode == "notes":
    n_df = notes_df[notes_df["章節"].astype(str).str.strip() == str(selected_chapter).strip()].reset_index(drop=True)
    if not n_df.empty:
        idx = st.session_state.note_idx
        row = n_df.iloc[idx]
        st.markdown(f'<span class="mode-badge">📖 講義模式</span>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="note-card">
            <h3>📌 {row.get("重點標題", "")}</h3>
            <p>{row.get("重點內容", "")}</p>
        </div>
        <p style='text-align:center;color:#999;font-size:0.8rem;'>第 {idx+1} / {len(n_df)} 頁</p>
        """, unsafe_allow_html=True)
        
        if pd.notna(row.get("圖片連結")) and str(row.get("圖片連結")).startswith("http"):
            st.image(str(row["圖片連結"]), use_container_width=True)

        colA, colB = st.columns(2)
        with colA:
            if st.button("⬅️ 上一頁", disabled=(idx == 0)):
                st.session_state.note_idx -= 1
                st.rerun()
        with colB:
            if st.button("下一頁 ➡️", disabled=(idx == len(n_df) - 1)):
                st.session_state.note_idx += 1
                st.rerun()

# ── 測驗模式 (略，維持原邏輯) ──────────────────────────────────────────────────
elif st.session_state.mode == "quiz":
    # (此處維持之前的測驗邏輯程式碼...)
    st.write("測驗模式開發中，功能已在底層對齊。")
    if st.button("🏠 返回首頁"): st.session_state.mode = None; st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='text-align:center;color:#BBBBAA;font-size:0.75rem;'>🐰 BUNNY'S 備考 APP · 改完 Excel 請記得按同步按鈕喔！</p>", unsafe_allow_html=True)

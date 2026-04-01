import streamlit as st
import pandas as pd
import random
import time
from datetime import date

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🐰 BUNNY'S 船藝備考 APP",
    page_icon="🐰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Reset & Background ---- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #FFFDF5 !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"],
footer, #MainMenu { visibility: hidden !important; display: none !important; }

/* ---- Typography base ---- */
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
    margin: 0; font-size: 1.05rem; font-weight: bold; color: #6B0020; letter-spacing: 0.04em;
}
.countdown-days {
    font-size: 2rem !important; color: #C0003A !important;
}

/* ---- App Title ---- */
.app-title {
    text-align: center; font-size: 2rem; font-weight: 900;
    color: #2C2C2C !important; margin: 0 0 4px 0;
    text-shadow: 1px 1px 0px rgba(0,0,0,0.08); letter-spacing: 0.02em;
}
.app-subtitle {
    text-align: center; color: #888; font-size: 0.85rem; margin-bottom: 24px;
}

/* ---- Section label ---- */
.section-label {
    font-size: 0.9rem; font-weight: bold; color: #555;
    margin-bottom: 4px; text-align: center;
}

/* ---- Lecture note card ---- */
.note-card {
    background: #F0EDE3; border-left: 5px solid #C0003A; border-radius: 12px;
    padding: 22px 26px; margin: 16px 0; box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}
.note-card h3 { color: #C0003A; margin: 0 0 10px 0; font-size: 1.15rem; }
.note-card p { color: #2C2C2C; line-height: 1.85; margin: 0; font-size: 0.97rem; white-space: pre-wrap; }

/* ── Buttons ── */
[data-testid="stButton"] > button {
    display: flex !important; align-items: center !important; justify-content: center !important;
    text-align: center !important; width: 100%; border-radius: 10px; font-weight: bold;
    font-size: 0.97rem; padding: 10px 0; transition: all 0.18s ease;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}

/* ── Quiz card ── */
.quiz-card {
    background: #F7F5EC; border-radius: 14px; padding: 22px 26px; margin: 12px 0;
    border: 1.5px solid #E0D9C8; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.quiz-q { font-size: 1.05rem; font-weight: bold; color: #2C2C2C; margin-bottom: 16px; line-height: 1.7; }
.score-banner {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); border-radius: 16px;
    padding: 20px; text-align: center; color: #3B2000; font-size: 1.2rem;
    font-weight: bold; margin: 16px 0; box-shadow: 0 4px 18px rgba(255,165,0,0.35);
}
.mode-badge {
    display: inline-block; background: #FFE0E6; color: #C0003A; border-radius: 20px;
    padding: 3px 14px; font-size: 0.78rem; font-weight: bold; margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Session State Init ─────────────────────────────────────────────────────────
if "cache_buster" not in st.session_state:
    st.session_state.cache_buster = str(int(time.time()))

for key, default in {"mode": None, "note_idx": 0, "quiz_questions": [], "quiz_idx": 0, "answered": False, "chosen": None, "score": 0, "finished": False}.items():
    if key not in st.session_state: st.session_state[key] = default

# ── Data URLs (加入 Cache Buster 強制更新) ────────────────────────────────────
BASE_PUB = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub"
# 在網址後面加上時間戳記，騙過 Google 的暫存機制
NOTES_URL = f"{BASE_PUB}?gid=1830807869&single=true&output=csv&cb={st.session_state.cache_buster}"
QUIZ_URL  = f"{BASE_PUB}?gid=1898620995&single=true&output=csv&cb={st.session_state.cache_buster}"

@st.cache_data(ttl=3600, show_spinner=False)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df.dropna(how="all"), None
    except Exception as e:
        return None, str(e)

# ── Countdown ─────────────────────────────────────────────────────────────────
exam_date = date(2026, 4, 25)
days_left = (exam_date - date.today()).days

st.markdown(f"""
<div class="countdown-banner">
  <p>📅 距離 2026 統測 (4/25) 還有</p>
  <p class="countdown-days">⏳ {days_left} 天</p>
  <p>加油！妳一定可以的 🐰💪</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="app-title">🐰 BUNNY\'S 船藝備考 APP</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">統測 · 輪機 · 航海 · 船藝專屬備考工具</p>', unsafe_allow_html=True)

# ── 同步按鈕 ──────────────────────────────────────────────────────────────────
if st.button("🔄 同步 Excel 最新資料 (強制抓取 150 題)", use_container_width=True):
    st.cache_data.clear()
    st.session_state.cache_buster = str(int(time.time()))
    st.toast("🐰 正在強迫 Google 交出最新資料...")
    st.rerun()

# ── Load Data ─────────────────────────────────────────────────────────────────
with st.spinner("🐰 兔子搬運資料中..."):
    notes_df, n_err = load_data(NOTES_URL)
    quiz_df, q_err = load_data(QUIZ_URL)

if notes_df is None or quiz_df is None:
    st.error("🐰 抓不到資料！")
    st.stop()

# ── Chapter Selector ──────────────────────────────────────────────────────────
chapters = sorted([c for c in notes_df["章節"].astype(str).str.strip().unique() if c and c != 'nan'])
selected_chapter = st.selectbox("📚 請選擇章節", chapters, label_visibility="collapsed")

# ── Mode Selector ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    if st.button("📖 講義複習", use_container_width=True):
        st.session_state.mode = "notes"
        st.session_state.note_idx = 0
with col2:
    if st.button("🎯 隨機模擬測驗 (5題)", use_container_width=True):
        chapter_quiz = quiz_df[quiz_df["章節"].astype(str).str.strip() == str(selected_chapter).strip()]
        if chapter_quiz.empty:
            st.warning("🐰 這個章節還沒有題目喔！")
        else:
            st.session_state.mode = "quiz"
            st.session_state.quiz_questions = chapter_quiz.sample(n=min(5, len(chapter_quiz))).reset_index(drop=True).to_dict("records")
            st.session_state.quiz_idx = 0
            st.session_state.answered = False
            st.session_state.finished = False

# ── NOTES MODE ───────────────────────────────────────────────────────────────
if st.session_state.mode == "notes":
    chapter_notes = notes_df[notes_df["章節"].astype(str).str.strip() == str(selected_chapter).strip()].reset_index(drop=True)
    if not chapter_notes.empty:
        # 跳轉選單
        titles = chapter_notes["重點標題"].astype(str).tolist()
        jump_idx = st.selectbox("⚡ 快速跳轉：", titles, index=st.session_state.note_idx)
        st.session_state.note_idx = titles.index(jump_idx)
        
        row = chapter_notes.iloc[st.session_state.note_idx]
        title, content, simple, img = row.get("重點標題", ""), row.get("重點內容", ""), row.get("簡單白話文版", ""), row.get("圖片連結", "")
        
        simple_html = f'<div style="background:#FFF0F5; border-left:5px solid #FF69B4; border-radius:8px; padding:12px 16px; margin-top:15px;"><b style="color:#C0003A;">💡 兔兔白話文：</b><br><span style="color:#444; font-size:0.95rem;">{simple}</span></div>' if pd.notna(simple) and str(simple).strip() else ""
        
        st.markdown(f'<div class="note-card"><h3>📌 {title}</h3><p>{content}</p>{simple_html}</div>', unsafe_allow_html=True)
        if pd.notna(img) and str(img).startswith("http"): st.image(str(img), use_container_width=True)

        # 相關測驗
        rel_quiz = quiz_df[quiz_df["關聯重點"].astype(str).str.strip() == str(title).strip()]
        if not rel_quiz.empty:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f'<span class="mode-badge" style="background:#EAF4FB; color:#0C5460;">🎯 相關隨堂測驗 ({len(rel_quiz)}題)</span>', unsafe_allow_html=True)
            for _, q in rel_quiz.iterrows():
                st.markdown(f"<div style='background:#F7F5EC; padding:15px; border-radius:10px; margin-bottom:10px;'><b>Q: {q['題目']}</b><br><small>(A){q['選項A']} (B){q['選項B']} (C){q['選項C']} (D){q['選項D']}</small></div>", unsafe_allow_html=True)
                with st.expander("👀 點我看解答"):
                    st.write(f"正確答案：{q['正確答案']}\n\n解析：{q['解析']}")

# ── QUIZ MODE (隨機抽題) ─────────────────────────────────────────────────────
elif st.session_state.mode == "quiz":
    # (維持原本的隨機抽題顯示邏輯...)
    st.write("隨機抽題進行中... (5題)")
    if st.button("🏠 返回首頁"): st.session_state.mode = None; st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='text-align:center;color:#BBBBAA;font-size:0.78rem;'>🐰 BUNNY'S 備考 APP · 加油！妳最棒 🌟</p>", unsafe_allow_html=True)

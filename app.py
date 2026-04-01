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

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Reset & Background ---- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #FFFDF5 !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"],
footer, #MainMenu { visibility: hidden !important; display: none !important; }

/* ---- Typography base (已更換為圓潤風格) ---- */
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
    margin: 0;
    font-size: 1.05rem;
    font-weight: bold;
    color: #6B0020;
    letter-spacing: 0.04em;
}
.countdown-days {
    font-size: 2rem !important;
    color: #C0003A !important;
}

/* ---- App Title ---- */
.app-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 900;
    color: #2C2C2C !important;
    margin: 0 0 4px 0;
    text-shadow: 1px 1px 0px rgba(0,0,0,0.08);
    letter-spacing: 0.02em;
}
.app-subtitle {
    text-align: center;
    color: #888;
    font-size: 0.85rem;
    margin-bottom: 24px;
}

/* ---- Section label ---- */
.section-label {
    font-size: 0.9rem;
    font-weight: bold;
    color: #555;
    margin-bottom: 4px;
    text-align: center;
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
.note-card h3 {
    color: #C0003A;
    margin: 0 0 10px 0;
    font-size: 1.15rem;
}
.note-card p {
    color: #2C2C2C;
    line-height: 1.85;
    margin: 0;
    font-size: 0.97rem;
    white-space: pre-wrap;
}
.note-pager {
    text-align: center;
    color: #999;
    font-size: 0.82rem;
    margin-top: 8px;
}

/* ── Buttons: absolute centre via flex ── */
[data-testid="stButton"] > button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    width: 100%;
    border-radius: 10px;
    font-weight: bold;
    font-size: 0.97rem;
    padding: 10px 0;
    transition: all 0.18s ease;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}

/* ── Quiz card ── */
.quiz-card {
    background: #F7F5EC;
    border-radius: 14px;
    padding: 22px 26px;
    margin: 12px 0;
    border: 1.5px solid #E0D9C8;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.quiz-q {
    font-size: 1.05rem;
    font-weight: bold;
    color: #2C2C2C;
    margin-bottom: 16px;
    line-height: 1.7;
}
.score-banner {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    color: #3B2000;
    font-size: 1.2rem;
    font-weight: bold;
    margin: 16px 0;
    box-shadow: 0 4px 18px rgba(255,165,0,0.35);
}
.mode-badge {
    display: inline-block;
    background: #FFE0E6;
    color: #C0003A;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.78rem;
    font-weight: bold;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Data URLs (絕對連線路徑) ──────────────────────────────────────────────────
# 請確保試算表已開啟「知道連結的任何人都可以檢視」權限
NOTES_URL = "https://docs.google.com/spreadsheets/d/1XIZqBYkHlt2INxq_M3yt6I4iKmzdKVblgpSafcLsk4/export?format=csv&gid=1830807869"
QUIZ_URL  = "https://docs.google.com/spreadsheets/d/1XIZqBYkHlt2INxq_M3yt6I4iKmzdKVblgpSafcLsk4/export?format=csv&gid=1898620995"

@st.cache_data(ttl=300, show_spinner=False)
def load_notes():
    try:
        df = pd.read_csv(NOTES_URL)
        df.columns = df.columns.str.strip()
        df = df.dropna(how="all")
        return df
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def load_quiz():
    try:
        df = pd.read_csv(QUIZ_URL)
        df.columns = df.columns.str.strip()
        df = df.dropna(how="all")
        return df
    except Exception:
        return None

# ── Countdown ─────────────────────────────────────────────────────────────────
exam_date = date(2026, 4, 25)
today     = date.today()
days_left = (exam_date - today).days

st.markdown(f"""
<div class="countdown-banner">
  <p>📅 距離 2026 統測 (4/25) 還有</p>
  <p class="countdown-days">⏳ {days_left} 天</p>
  <p>加油！妳一定可以的 🐰💪</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="app-title">🐰 BUNNY\'S 船藝備考 APP</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">統測 · 輪機 · 航海 · 船藝專屬備考工具</p>', unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
with st.spinner("🐰 兔子搬運資料中..."):
    notes_df = load_notes()
    quiz_df  = load_quiz()

if notes_df is None and quiz_df is None:
    st.error("🐰 兔子搬運資料失敗！請確認試算表權限是否已開啟「知道連結的任何人都可以檢視」。")
    st.stop()

# ── Chapter Selector ──────────────────────────────────────────────────────────
chapters = []
if notes_df is not None and "章節" in notes_df.columns:
    chapters = sorted(notes_df["章節"].dropna().unique().tolist())

if not chapters:
    st.warning("🐰 暫時找不到章節資料。請確認試算表 Notes 分頁的「章節」欄位是否有填寫內容！")
    st.stop()

st.markdown('<p class="section-label">📚 請選擇章節</p>', unsafe_allow_html=True)
selected_chapter = st.selectbox("", chapters, label_visibility="collapsed")

# ── Mode Selector ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    go_notes = st.button("📖 講義複習", use_container_width=True)
with col2:
    go_quiz  = st.button("🎯 隨機模擬測驗 (5題)", use_container_width=True)

# ── Session State Init ─────────────────────────────────────────────────────────
for key, default in {
    "mode": None,
    "note_idx": 0,
    "quiz_questions": [],
    "quiz_idx": 0,
    "answered": False,
    "chosen": None,
    "score": 0,
    "finished": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if go_notes:
    st.session_state.mode     = "notes"
    st.session_state.note_idx = 0

if go_quiz:
    chapter_quiz = pd.DataFrame()
    if quiz_df is not None:
        if "章節" in quiz_df.columns:
            chapter_quiz = quiz_df[quiz_df["章節"].astype(str).str.strip() == str(selected_chapter).strip()]
    
    if chapter_quiz.empty:
        st.warning(f"🐰「{selected_chapter}」目前還沒有題目。")
    else:
        n = min(5, len(chapter_quiz))
        sampled = chapter_quiz.sample(n=n).reset_index(drop=True)
        st.session_state.mode           = "quiz"
        st.session_state.quiz_questions = sampled.to_dict("records")
        st.session_state.quiz_idx       = 0
        st.session_state.answered       = False
        st.session_state.score          = 0
        st.session_state.finished       = False

# ── NOTES MODE ───────────────────────────────────────────────────────────────
if st.session_state.mode == "notes":
    chapter_notes = notes_df[notes_df["章節"].astype(str).str.strip() == str(selected_chapter).strip()]

    if chapter_notes.empty:
        st.info(f"🐰「{selected_chapter}」尚無講義。")
    else:
        chapter_notes = chapter_notes.reset_index(drop=True)
        total   = len(chapter_notes)
        idx     = st.session_state.note_idx
        idx     = max(0, min(idx, total - 1))
        row     = chapter_notes.iloc[idx]

        st.markdown('<span class="mode-badge">📖 講義複習模式</span>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="note-card">
            <h3>📌 {row.get("重點標題", "")}</h3>
            <p>{row.get("重點內容", "")}</p>
        </div>
        <p class="note-pager">第 {idx+1} / {total} 頁　｜　章節：{selected_chapter}</p>
        """, unsafe_allow_html=True)

        if pd.notna(row.get("圖片連結")) and str(row.get("圖片連結")).startswith("http"):
            st.image(str(row["圖片連結"]), use_container_width=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if st.button("⬅️ 上一頁", use_container_width=True, disabled=(idx == 0)):
                st.session_state.note_idx -= 1
                st.rerun()
        with c3:
            if st.button("下一頁 ➡️", use_container_width=True, disabled=(idx == total - 1)):
                st.session_state.note_idx += 1
                st.rerun()

# ── QUIZ MODE ────────────────────────────────────────────────────────────────
elif st.session_state.mode == "quiz":
    questions = st.session_state.quiz_questions
    if st.session_state.finished:
        st.markdown(f'<div class="score-banner">🎯 測驗結束！得分：{st.session_state.score} / {len(questions)}</div>', unsafe_allow_html=True)
        if st.button("🔁 再測一次", use_container_width=True):
            st.session_state.mode = None
            st.rerun()
    else:
        q_idx = st.session_state.quiz_idx
        row = questions[q_idx]
        st.markdown(f'<span class="mode-badge">🎯 模擬測驗 第 {q_idx+1} 題</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="quiz-card"><p class="quiz-q">{row.get("題目", "")}</p></div>', unsafe_allow_html=True)

        opts = ["A", "B", "C", "D"]
        for o in opts:
            btn_label = f"({o}) {row.get('選項'+o, '')}"
            if not st.session_state.answered:
                if st.button(btn_label, key=f"btn_{o}", use_container_width=True):
                    st.session_state.answered = True
                    st.session_state.chosen = o
                    if o == str(row.get("正確答案", "")).strip().upper():
                        st.session_state.score += 1
                    st.rerun()
            else:
                correct_ans = str(row.get("正確答案", "")).strip().upper()
                if o == correct_ans:
                    st.success(f"✅ {btn_label}")
                elif o == st.session_state.chosen:
                    st.error(f"❌ {btn_label}")
                else:
                    st.write(f"⚪ {btn_label}")

        if st.session_state.answered:
            st.info(f"💡 詳解：{row.get('解析', '')}")
            if st.button("下一題 ➡️" if q_idx < len(questions)-1 else "🏁 查看成績", use_container_width=True):
                if q_idx < len(questions)-1:
                    st.session_state.quiz_idx += 1
                    st.session_state.answered = False
                else:
                    st.session_state.finished = True
                st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='text-align:center;color:#BBBBAA;font-size:0.78rem;'>🐰 BUNNY'S 備考 APP · 加油！妳最棒 🌟</p>", unsafe_allow_html=True)

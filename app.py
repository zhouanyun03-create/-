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

# ── Data URLs ─────────────────────────────────────────────────────────────────
BASE_PUB = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub"
NOTES_URL = f"{BASE_PUB}?gid=1830807869&single=true&output=csv"
QUIZ_URL  = f"{BASE_PUB}?gid=1898620995&single=true&output=csv"

# ⚠️ 將快取時間拉長到 3600 秒 (1小時)，防止 Google 伺服器新舊資料亂跳
@st.cache_data(ttl=3600, show_spinner=False)
def load_notes():
    try:
        df = pd.read_csv(NOTES_URL)
        df.columns = df.columns.str.strip()
        df = df.dropna(how="all")
        return df, None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=3600, show_spinner=False)
def load_quiz():
    try:
        df = pd.read_csv(QUIZ_URL)
        df.columns = df.columns.str.strip()
        df = df.dropna(how="all")
        return df, None
    except Exception as e:
        return None, str(e)

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

# ── 同步按鈕 ──────────────────────────────────────────────────────────────────
if st.button("🔄 同步 Excel 最新資料", use_container_width=True):
    st.cache_data.clear()
    st.toast("🐰 已清空舊記憶，正在抓取最新資料...")
    st.rerun()

# ── Load Data ─────────────────────────────────────────────────────────────────
with st.spinner("🐰 兔子搬運資料中..."):
    notes_df, notes_err = load_notes()
    quiz_df, quiz_err  = load_quiz()

if notes_df is None or quiz_df is None:
    st.error("🐰 兔子連線被 Google 擋住了！請看下方的真實錯誤原因：")
    if notes_err: st.code(f"【講義分頁錯誤】: {notes_err}")
    if quiz_err: st.code(f"【題庫分頁錯誤】: {quiz_err}")
    st.stop()

# ── Chapter Selector ──────────────────────────────────────────────────────────
chapters = []
if "章節" in notes_df.columns:
    notes_df["章節"] = notes_df["章節"].astype(str).str.strip()
    chapters = sorted([c for c in notes_df["章節"].unique() if c and c.lower() != 'nan'])

if not chapters:
    st.warning("🐰 暫時找不到章節資料。請確認試算表 Notes 分頁的「章節」欄位有填寫內容！")
    st.stop()

st.markdown('<p class="section-label">📚 請選擇章節</p>', unsafe_allow_html=True)
selected_chapter = st.selectbox("", chapters, label_visibility="collapsed")

# ── Mode Selector ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1: go_notes = st.button("📖 講義複習", use_container_width=True)
with col2: go_quiz  = st.button("🎯 隨機模擬測驗 (5題)", use_container_width=True)

# ── Session State Init ─────────────────────────────────────────────────────────
for key, default in {"mode": None, "note_idx": 0, "quiz_questions": [], "quiz_idx": 0, "answered": False, "chosen": None, "score": 0, "finished": False}.items():
    if key not in st.session_state: st.session_state[key] = default

if go_notes:
    st.session_state.mode     = "notes"
    st.session_state.note_idx = 0

if go_quiz:
    chapter_quiz = pd.DataFrame()
    if "章節" in quiz_df.columns:
        quiz_df["章節"] = quiz_df["章節"].astype(str).str.strip()
        chapter_quiz = quiz_df[quiz_df["章節"] == str(selected_chapter)]
        
    if chapter_quiz.empty:
        chapter_quiz = quiz_df[quiz_df.iloc[:, 0].astype(str).str.strip() == str(selected_chapter)]

    if chapter_quiz.empty:
        st.warning(f"🐰「{selected_chapter}」目前還沒有題目。")
    else:
        n = min(5, len(chapter_quiz))
        st.session_state.mode           = "quiz"
        st.session_state.quiz_questions = chapter_quiz.sample(n=n).reset_index(drop=True).to_dict("records")
        st.session_state.quiz_idx       = 0
        st.session_state.answered       = False
        st.session_state.chosen         = None
        st.session_state.score          = 0
        st.session_state.finished       = False

# ── NOTES MODE ───────────────────────────────────────────────────────────────
if st.session_state.mode == "notes":
    chapter_notes = notes_df[notes_df["章節"] == str(selected_chapter)]

    if chapter_notes.empty:
        st.info(f"🐰「{selected_chapter}」尚無講義。")
    else:
        chapter_notes = chapter_notes.reset_index(drop=True)
        total   = len(chapter_notes)
        idx     = st.session_state.note_idx
        idx     = max(0, min(idx, total - 1))
        row     = chapter_notes.iloc[idx]

        st.markdown('<span class="mode-badge">📖 講義複習模式</span>', unsafe_allow_html=True)
        
        # 取得各欄位資料，這次保證抓的是 "簡單白話文版"
        title   = row.get("重點標題", "")
        content = row.get("重點內容", "")
        simple  = row.get("簡單白話文版", "")
        img_url = row.get("圖片連結", "")

        # 如果有填寫「簡單白話文版」，就生成一個可愛的粉紅小提示框
        simple_html = ""
        if pd.notna(simple) and str(simple).strip():
            simple_html = f'<div style="background: #FFF0F5; border-left: 5px solid #FF69B4; border-radius: 8px; padding: 12px 16px; margin-top: 15px;"><b style="color: #C0003A;">💡 兔兔白話文：</b><br><span style="color: #444; font-size: 0.95rem; line-height: 1.6;">{simple}</span></div>'

        st.markdown(f'<div class="note-card"><h3 style="color:#C0003A;margin:0 0 10px 0;font-size:1.15rem;">📌 {title}</h3><p style="color:#2C2C2C;line-height:1.85;margin:0;font-size:0.97rem;white-space:pre-wrap;">{content}</p>{simple_html}</div><p style="text-align:center;color:#999;font-size:0.82rem;margin-top:8px;">第 {idx+1} / {total} 頁　｜　章節：{selected_chapter}</p>', unsafe_allow_html=True)

        if pd.notna(img_url) and str(img_url).startswith("http"):
            st.image(str(img_url), use_container_width=True)

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
        total_q = len(questions)
        score   = st.session_state.score
        pct     = round(score / total_q * 100) if total_q > 0 else 0
        emoji   = "🏆" if pct >= 80 else ("🐰" if pct >= 60 else "😅")
        msg     = "太厲害了！🎉 繼續保持！" if pct >= 80 else ("不錯喔！再複習一下薄弱的地方 💪" if pct >= 60 else "別灰心！再看看講義，一定進步 🌟")
        
        st.markdown(f"""
        <div class="score-banner">
            {emoji} 測驗結束！<br>
            得分：{score} / {total_q}　（{pct}%）<br>
            <span style="font-size:1rem;">{msg}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔁 返回首頁", use_container_width=True):
            st.session_state.mode = None
            st.rerun()
    else:
        q_idx   = st.session_state.quiz_idx
        row     = questions[q_idx]
        total_q = len(questions)

        def get_col(row_data, *candidates):
            for c in candidates:
                if c in row_data and pd.notna(row_data[c]) and str(row_data[c]).strip():
                    return str(row_data[c]).strip()
            return ""

        question    = get_col(row, "題目", "question", "Question")
        opt_a       = get_col(row, "選項A", "A", "a", "option_a")
        opt_b       = get_col(row, "選項B", "B", "b", "option_b")
        opt_c       = get_col(row, "選項C", "C", "c", "option_c")
        opt_d       = get_col(row, "選項D", "D", "d", "option_d")
        answer      = get_col(row, "正確答案", "答案", "answer", "Answer")
        explanation = get_col(row, "解析", "解說", "詳解", "explanation", "說明")

        options = {}
        if opt_a: options["A"] = opt_a
        if opt_b: options["B"] = opt_b
        if opt_c: options["C"] = opt_c
        if opt_d: options["D"] = opt_d

        st.markdown(f'<span class="mode-badge">🎯 模擬測驗模式　第 {q_idx+1} / {total_q} 題</span>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="quiz-card">
            <p class="quiz-q">Q{q_idx+1}. {question}</p>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.answered:
            for key, text in options.items():
                if st.button(f"({key}) {text}", key=f"opt_{key}", use_container_width=True):
                    st.session_state.chosen   = key
                    st.session_state.answered = True
                    if key.upper() == answer.upper():
                        st.session_state.score += 1
                    st.rerun()
        else:
            chosen     = st.session_state.chosen
            is_correct = (chosen.upper() == answer.upper())

            for key, text in options.items():
                label = f"({key}) {text}"
                if key.upper() == answer.upper():
                    st.markdown(f"<div style='background:#D4EDDA;border-radius:8px;padding:9px 14px;margin:4px 0;color:#155724;font-weight:bold;display:flex;justify-content:center;text-align:center'>✅ {label}</div>", unsafe_allow_html=True)
                elif key == chosen and not is_correct:
                    st.markdown(f"<div style='background:#F8D7DA;border-radius:8px;padding:9px 14px;margin:4px 0;color:#721C24;font-weight:bold;display:flex;justify-content:center;text-align:center'>❌ {label}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background:#F0EDE3;border-radius:8px;padding:9px 14px;margin:4px 0;color:#555;display:flex;justify-content:center;text-align:center'>{label}</div>", unsafe_allow_html=True)

            if is_correct:
                st.markdown('<div class="correct-feedback">🎉 答對了！太棒了！</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="wrong-feedback">😢 答錯了！正確答案是 <b>({answer})</b></div>', unsafe_allow_html=True)

            if explanation:
                st.markdown(f'<div style="background:#EAF4FB;border-left:5px solid #17A2B8;border-radius:8px;padding:12px 16px;color:#0C5460;margin-top:8px;font-size:0.91rem;">💡 <b>詳解：</b>{explanation}</div>', unsafe_allow_html=True)

            if q_idx + 1 < total_q:
                if st.button("下一題 ➡️", use_container_width=True):
                    st.session_state.quiz_idx += 1
                    st.session_state.answered  = False
                    st.session_state.chosen    = None
                    st.rerun()
            else:
                if st.button("🏁 查看成績", use_container_width=True):
                    st.session_state.finished = True
                    st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='text-align:center;color:#BBBBAA;font-size:0.78rem;'>🐰 BUNNY'S 備考 APP · 加油！妳最棒 🌟</p>", unsafe_allow_html=True)

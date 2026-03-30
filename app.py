import streamlit as st
import pandas as pd

# ══════════════════════════════════════════════════════════════
#  頁面設定（必須最先呼叫）
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="✨ 刷題小精靈",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
#  全域 CSS — 強制淺色、大圓角、立體感
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');

/* ── 強制淺色底 ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main, .block-container,
[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background-color: #FFFDF5 !important;
    color: #444444 !important;
    font-family: 'Noto Sans TC', sans-serif !important;
}

/* 隱藏 Streamlit 預設 UI 雜訊 */
#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { visibility: hidden; }

/* ── 主內容區 ── */
.block-container {
    max-width: 820px;
    padding: 2rem 2.5rem 5rem !important;
}

/* ── 側邊欄整體 ── */
[data-testid="stSidebar"] {
    border-right: 1px solid #F0E6D3 !important;
}
[data-testid="stSidebarContent"] {
    padding: 1.6rem 1.2rem !important;
}

/* 側邊欄選單標題 */
.sidebar-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #FFB7C5;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* 側邊欄 selectbox 卡片化 */
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1px solid #EEEEEE !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 10px rgba(92,61,46,0.07) !important;
    color: #444444 !important;
}

/* 側邊欄分隔線 */
.sidebar-divider {
    border: none;
    border-top: 1px dashed #E8D8C4;
    margin: 1.2rem 0;
}

/* 側邊欄得分卡 */
.sidebar-score {
    background: linear-gradient(135deg, #FFF3E8, #FFEEF5);
    border-radius: 20px;
    border: 1px solid #F0D8C8;
    padding: 1rem 1.2rem;
    text-align: center;
    margin-top: 1rem;
}
.sidebar-score-num {
    font-size: 2.2rem;
    font-weight: 900;
    color: #E07A5F;
    line-height: 1;
}
.sidebar-score-label {
    font-size: 0.8rem;
    color: #A08060;
    margin-top: 0.2rem;
}

/* ── 進度條（粉綠色） ── */
.progress-wrap {
    background: #E8F5E9;
    border-radius: 999px;
    height: 16px;
    margin: 0.8rem 0 0.3rem;
    overflow: hidden;
    box-shadow: inset 0 1px 4px rgba(0,0,0,0.06);
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #A8E6CF, #56C596);
    transition: width 0.5s cubic-bezier(.4,0,.2,1);
    position: relative;
}
.progress-fill::after {
    content: '';
    position: absolute;
    top: 3px; left: 8px; right: 8px; height: 4px;
    background: rgba(255,255,255,0.45);
    border-radius: 999px;
}
.progress-label {
    text-align: right;
    font-size: 0.82rem;
    color: #7CB99A;
    margin-bottom: 1rem;
    font-weight: 500;
}

/* ── 題目卡片 ── */
.question-card {
    background: #FFFFFF;
    border: 1px solid #EEEEEE;
    border-radius: 24px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(92,61,46,0.07);
}
.chapter-badge {
    display: inline-block;
    background: linear-gradient(90deg, #A8E6CF, #7BB8F5);
    color: #FFFFFF;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.8rem;
    border-radius: 999px;
    margin-bottom: 0.6rem;
}
.question-number {
    font-size: 0.78rem;
    font-weight: 700;
    color: #FFB7C5;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.question-text {
    font-size: 1.15rem;
    font-weight: 600;
    color: #333333;
    line-height: 1.75;
}

/* ── 選項按鈕 ── */
div.stButton > button {
    width: 100%;
    text-align: left;
    background: #F9F9F9 !important;
    border: 1px solid #EEEEEE !important;
    border-radius: 20px !important;
    padding: 0.85rem 1.4rem !important;
    font-size: 1rem !important;
    color: #444444 !important;
    font-family: 'Noto Sans TC', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.18s ease !important;
    margin-bottom: 0.4rem !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06), 0 1px 0 rgba(255,255,255,0.8) inset !important;
    cursor: pointer;
}
div.stButton > button:hover {
    background: #FFF3E8 !important;
    border-color: #FFB7C5 !important;
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 6px 20px rgba(255,183,197,0.3), 0 2px 0 rgba(255,255,255,0.8) inset !important;
}
div.stButton > button:active {
    transform: translateY(0px) scale(0.99) !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}

/* 下一題按鈕 */
.btn-next > div > div.stButton > button,
.btn-next > div.stButton > button {
    background: linear-gradient(135deg, #A8E6CF, #56C596) !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(86,197,150,0.4) !important;
}
.btn-next > div > div.stButton > button:hover,
.btn-next > div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(86,197,150,0.5) !important;
}

/* 重新開始按鈕 */
.btn-restart > div > div.stButton > button,
.btn-restart > div.stButton > button {
    background: #FFFFFF !important;
    border: 1px solid #DDDDDD !important;
    color: #999999 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}

/* ── 解析區塊 ── */
.explanation-correct {
    background: #EDF5FF;
    border: 1px solid #B8D8F8;
    border-radius: 20px;
    padding: 1.2rem 1.6rem;
    margin-top: 0.8rem;
    font-size: 0.95rem;
    color: #2C4870;
    line-height: 1.8;
}
.explanation-wrong {
    background: #FFF0F4;
    border: 1px solid #FFB7C5;
    border-radius: 20px;
    padding: 1.2rem 1.6rem;
    margin-top: 0.8rem;
    font-size: 0.95rem;
    color: #7A2C3E;
    line-height: 1.8;
}
.explanation-title {
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

/* ── 得分結束畫面 ── */
.score-card {
    background: linear-gradient(135deg, #FFF3E8 0%, #FFEEF5 100%);
    border-radius: 28px;
    padding: 3rem 2rem;
    text-align: center;
    border: 1px solid #F0D8C8;
    box-shadow: 0 8px 30px rgba(224,122,95,0.12);
}
.score-big {
    font-size: 5rem;
    font-weight: 900;
    color: #E07A5F;
    line-height: 1;
}
.score-desc {
    font-size: 1.05rem;
    color: #8B5E3C;
    margin-top: 0.6rem;
}

/* 標題區 */
.app-header { text-align:center; padding: 0.5rem 0 0.2rem; }
.app-title  { font-size:2rem; font-weight:900; color:#5C3D2E; letter-spacing:0.05em; }
.app-subtitle { font-size:0.92rem; color:#A08060; margin-top:0.15rem; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  資料載入
# ══════════════════════════════════════════════════════════════
CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-"
    "da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub?output=csv"
)

@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(CSV_URL, encoding="utf-8")
    df.columns = df.columns.str.strip()
    return df

try:
    df_all = load_data()
except Exception:
    st.markdown("""
    <div class="question-card" style="text-align:center;padding:3rem;">
        <div style="font-size:3rem;">🧚</div>
        <div style="font-size:1.1rem;color:#8B5E3C;margin-top:0.8rem;">
            小精靈正在努力連線中，請稍候…
        </div>
        <div style="font-size:0.82rem;color:#A08060;margin-top:0.4rem;">
            請確認網路連線或稍後再試
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── 欄位自動偵測（容錯映射）──
def find_col(df, *keywords):
    for kw in keywords:
        match = [c for c in df.columns if kw in c]
        if match:
            return match[0]
    return None

col_id      = find_col(df_all, "題號") or df_all.columns[0]
col_chapter = find_col(df_all, "章節", "Chapter")
col_q       = find_col(df_all, "題目") or df_all.columns[1]
col_a       = find_col(df_all, "選項A") or df_all.columns[2]
col_b       = find_col(df_all, "選項B") or df_all.columns[3]
col_c       = find_col(df_all, "選項C") or df_all.columns[4]
col_d       = find_col(df_all, "選項D") or df_all.columns[5]
col_ans     = find_col(df_all, "正確答案", "答案") or df_all.columns[6]
col_exp     = find_col(df_all, "解析") or df_all.columns[7]
col_img     = find_col(df_all, "圖片", "image", "Image", "img")

# ── 章節清單 ──
CHAPTERS_ALL = "📚 全部章節"
if col_chapter:
    chapters = [CHAPTERS_ALL] + sorted(df_all[col_chapter].dropna().unique().tolist())
else:
    chapters = [CHAPTERS_ALL]

# ══════════════════════════════════════════════════════════════
#  Session State 初始化
# ══════════════════════════════════════════════════════════════
def init_state(chapter=CHAPTERS_ALL):
    st.session_state.chapter  = chapter
    st.session_state.idx      = 0
    st.session_state.score    = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.finished = False

if "idx" not in st.session_state:
    init_state()

# ══════════════════════════════════════════════════════════════
#  左側邊欄
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="app-header">
        <div class="app-title">🌸 刷題<br>小精靈</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-title">🗂 選擇挑戰章節</div>', unsafe_allow_html=True)
    selected_chapter = st.selectbox(
        label="章節",
        options=chapters,
        index=chapters.index(st.session_state.get("chapter", CHAPTERS_ALL)),
        label_visibility="collapsed",
        key="chapter_select",
    )

    # 切換章節時重置
    if selected_chapter != st.session_state.chapter:
        init_state(selected_chapter)
        st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # 得分卡
    st.markdown(f"""
    <div class="sidebar-score">
        <div class="sidebar-score-num">💎 {st.session_state.score}</div>
        <div class="sidebar-score-label">本次得分</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="btn-restart">', unsafe_allow_html=True)
    if st.button("🔄 重新開始", key="sidebar_restart", use_container_width=True):
        init_state(st.session_state.chapter)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  篩選題目
# ══════════════════════════════════════════════════════════════
if col_chapter and st.session_state.chapter != CHAPTERS_ALL:
    df = df_all[df_all[col_chapter] == st.session_state.chapter].reset_index(drop=True)
else:
    df = df_all.reset_index(drop=True)

if len(df) == 0:
    st.warning("此章節目前沒有題目，請選擇其他章節 🌿")
    st.stop()

total = len(df)

# ══════════════════════════════════════════════════════════════
#  主標題
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="app-header">
    <div class="app-title">🌸 刷題小精靈</div>
    <div class="app-subtitle">每一題都是進步的足跡 ✨</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  結束畫面
# ══════════════════════════════════════════════════════════════
if st.session_state.finished:
    pct = int(st.session_state.score / total * 100)
    if pct >= 80:
        big_emoji, msg = "🎉", "太厲害了！繼續保持！"
    elif pct >= 60:
        big_emoji, msg = "💪", "不錯喔！再多練習一下！"
    else:
        big_emoji, msg = "📖", "再複習一遍，你一定可以！"

    st.markdown(f"""
    <div class="score-card">
        <div style="font-size:3.5rem;">{big_emoji}</div>
        <div class="score-big">{st.session_state.score}
            <span style="font-size:2rem;color:#C0927A;">/{total}</span>
        </div>
        <div class="score-desc">答對率 {pct}%　{msg}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="btn-next">', unsafe_allow_html=True)
    if st.button("🔄 再挑戰一次", key="restart_end", use_container_width=True):
        init_state(st.session_state.chapter)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════
#  進度條（粉綠）
# ══════════════════════════════════════════════════════════════
idx = st.session_state.idx
progress_pct = int(idx / total * 100)
st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-fill" style="width:{progress_pct}%;"></div>
</div>
<div class="progress-label">🌿 第 {idx + 1} 題 / 共 {total} 題</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  題目資料
# ══════════════════════════════════════════════════════════════
row     = df.iloc[idx]
q_num   = row[col_id]
q_text  = row[col_q]
opts    = {
    "A": str(row[col_a]),
    "B": str(row[col_b]),
    "C": str(row[col_c]),
    "D": str(row[col_d]),
}
correct = str(row[col_ans]).strip().upper()
explain = str(row[col_exp])
chapter_label = str(row[col_chapter]) if col_chapter else ""
img_url = (
    str(row[col_img]).strip()
    if col_img and pd.notna(row[col_img]) and str(row[col_img]).strip() not in ("", "nan")
    else ""
)

OPT_EMOJI = {"A": "🚢", "B": "⚓", "C": "🧭", "D": "🗺️"}

# ── 題目卡片 ──
badge_html = f'<span class="chapter-badge">{chapter_label}</span><br>' if chapter_label else ""
st.markdown(f"""
<div class="question-card">
    {badge_html}
    <div class="question-number">Q {q_num}</div>
    <div class="question-text">{q_text}</div>
</div>
""", unsafe_allow_html=True)

# ── 題目圖片（若有）──
if img_url:
    try:
        st.image(img_url, use_container_width=False)
    except Exception:
        pass  # 圖片載入失敗靜默跳過

# ══════════════════════════════════════════════════════════════
#  選項按鈕 / 結果
# ══════════════════════════════════════════════════════════════
if not st.session_state.answered:
    for key, val in opts.items():
        emoji = OPT_EMOJI.get(key, "🔹")
        if st.button(f"{emoji}  {key}｜{val}", key=f"opt_{key}", use_container_width=True):
            st.session_state.answered = True
            st.session_state.selected = key
            if key == correct:
                st.session_state.score += 1
            st.rerun()
else:
    sel = st.session_state.selected

    # ── 對 / 錯 回饋 ──
    if sel == correct:
        st.success(f"🎉 太棒了！你選對了！正確答案是 **{correct}**")
        st.balloons()
        explain_class = "explanation-correct"
        explain_title = "📝 詳細解析"
    else:
        st.error(f"這次選了 **{sel}**，正確答案是 **{correct}**，繼續加油！")
        explain_class = "explanation-wrong"
        explain_title = "💡 小精靈溫馨提示"

    # ── 解析區塊 ──
    st.markdown(f"""
    <div class="{explain_class}">
        <div class="explanation-title">{explain_title}</div>
        {explain}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<div class="btn-next">', unsafe_allow_html=True)
        if idx + 1 < total:
            if st.button("下一題 ➡️", key="next", use_container_width=True):
                st.session_state.idx      += 1
                st.session_state.answered  = False
                st.session_state.selected  = None
                st.rerun()
        else:
            if st.button("🏁 查看最終成績", key="finish", use_container_width=True):
                st.session_state.finished = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="btn-restart">', unsafe_allow_html=True)
        if st.button("🔄", key="restart_inline", use_container_width=True):
            init_state(st.session_state.chapter)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st
import pandas as pd

# 1. 頁面設定
st.set_page_config(page_title="✨ 刷題小精靈", page_icon="🌸", layout="wide")

# 2. 全域 CSS (解決黑色背景 & 可愛化)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
html, body, [data-testid="stAppViewContainer"] {
    background-color: #FFFDF5 !important;
    color: #444444 !important;
    font-family: 'Noto Sans TC', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { max-width: 600px; padding: 1rem !important; }
div[data-testid="stSelectbox"] > div { border-radius: 20px !important; }
div.stButton > button {
    width: 100%; border-radius: 18px !important;
    background: #F9F9F9 !important; border: 1px solid #EEEEEE !important;
    box-shadow: 0 3px 6px rgba(0,0,0,0.05) !important;
}
.question-card {
    background: white; border-radius: 24px; padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# 3. 資料載入
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    return df

try:
    df_all = load_data()
except:
    st.error("連線中...請稍候")
    st.stop()

# 4. 狀態初始化
if "idx" not in st.session_state:
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.chapter = "📚 全部章節"

# 5. 主畫面標題與選單
st.markdown("<h2 style='text-align:center;'>🌸 刷題小精靈</h2>", unsafe_allow_html=True)
all_chapters = ["📚 全部章節"] + sorted(df_all["章節"].dropna().unique().tolist())
selected_chapter = st.selectbox("📍 切換章節", all_chapters, index=all_chapters.index(st.session_state.chapter))

if selected_chapter != st.session_state.chapter:
    st.session_state.chapter = selected_chapter
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.rerun()

# 6. 篩選與進度
df = df_all if st.session_state.chapter == "📚 全部章節" else df_all[df_all["章節"] == st.session_state.chapter].reset_index(drop=True)
total = len(df)
idx = st.session_state.idx

st.progress(idx / total)
st.write(f"🌿 第 {idx+1} 題 / 共 {total} 題 (目前得分: {st.session_state.score})")

# 7. 顯示題目
row = df.iloc[idx]
st.markdown(f'<div class="question-card"><b>{row["題目"]}</b></div>', unsafe_allow_html=True)

if '圖片' in row and pd.notna(row['圖片']):
    st.image(row['圖片'])

# 8. 選項與邏輯
correct = str(row['正確答案']).strip().upper()
if not st.session_state.answered:
    for opt in ["A", "B", "C", "D"]:
        if st.button(f"{opt}｜{row['選項'+opt]}"):
            st.session_state.answered = True
            st.session_state.last_ans = opt
            if opt == correct: st.session_state.score += 1
            st.rerun()
else:
    if st.session_state.last_ans == correct:
        st.success("🎉 答對了！")
    else:
        st.error(f"❌ 答錯了，答案是 {correct}")
    st.info(f"💡 解析：{row['解析']}")
    if st.button("下一題 ➡️" if idx + 1 < total else "🏁 看成績"):
        if idx + 1 < total:
            st.session_state.idx += 1
            st.session_state.answered = False
        else:
            st.balloons()
            st.write(f"🎊 完成！得分：{st.session_state.score}/{total}")
        st.rerun()

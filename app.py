import streamlit as st
import pandas as pd

# 1. 頁面基本設定
st.set_page_config(page_title="🚢 船藝破關小精靈", page_icon="📖", layout="wide")

# 2. 可愛化 CSS (加入講義重點區塊樣式)
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
    
    /* 講義重點區塊 (灰色背景) */
    .handout-box {
        background-color: #F0F0F0; border-radius: 15px; padding: 20px;
        border-left: 8px solid #A8DADC; margin-bottom: 20px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    .question-box {
        background: white; border-radius: 20px; padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-top: 10px;
    }
    div.stButton > button {
        width: 100%; border-radius: 12px !important;
        background: #FFFFFF !important; transition: 0.2s;
    }
    div.stButton > button:hover { background: #F0FFF0 !important; border-color: #A8E6CF !important; }
</style>
""", unsafe_allow_html=True)

# 3. 資料讀取
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgUbGiwR1M1_BooQnDEPJjU2gm1sFLD3RKpz-da2Hhrj8-PNj09lGQJkdFmuG-3UvGOCZD1yg6LtNu/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    return df

try:
    df_all = load_data()
except:
    st.error("🧚 資料搬運中...")
    st.stop()

# 4. 初始化 Session State
if "mode" not in st.session_state: st.session_state.mode = "HOME"
if "chapter_progress" not in st.session_state: st.session_state.chapter_progress = {} # 儲存各章進度
if "answered" not in st.session_state: st.session_state.answered = False

# 5. 主選單畫面
if st.session_state.mode == "HOME":
    st.markdown("<h1 style='text-align:center;'>🌸 船藝破關小精靈</h1>", unsafe_allow_html=True)
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 進入學習模式\n(講義+測驗)", use_container_width=True):
            st.session_state.mode = "LEARN"
            st.rerun()
    with col2:
        if st.button("✍️ 純測驗模式\n(隨機題庫)", use_container_width=True):
            st.session_state.mode = "QUIZ"
            st.rerun()

# 6. 學習模式 (講義 + 關卡測驗)
elif st.session_state.mode == "LEARN":
    if st.button("⬅️ 返回主選單"):
        st.session_state.mode = "HOME"
        st.rerun()

    chapters = sorted(df_all["章節"].dropna().unique().tolist())
    curr_ch = st.selectbox("📍 選擇要學習的章節", chapters)
    
    # 取得該章節題目
    df_ch = df_all[df_all["章節"] == curr_ch].reset_index(drop=True)
    
    # 初始化該章進度 (若無則從第 0 題開始)
    if curr_ch not in st.session_state.chapter_progress:
        st.session_state.chapter_progress[curr_ch] = 0
    
    p_idx = st.session_state.chapter_progress[curr_ch]
    
    if p_idx < len(df_ch):
        row = df_ch.iloc[p_idx]
        
        # --- 講義區塊 ---
        st.subheader(f"📚 知識點 {p_idx + 1}")
        st.markdown(f"""<div class="handout-box"><b>💡 講義重點：</b><br><br>{row['解析']}</div>""", unsafe_allow_html=True)
        if '圖片' in row and pd.notna(row['圖片']):
            st.image(row['圖片'])
            
        st.write("---")
        
        # --- 測驗區塊 ---
        st.markdown(f"**📝 隨堂小測驗：**\n{row['題目']}")
        
        correct_ans = str(row['正確答案']).strip().upper()
        
        if not st.session_state.answered:
            for opt in ["A", "B", "C", "D"]:
                if st.button(f"{opt}｜{row[f'選項{opt}']}", key=f"learn_{p_idx}_{opt}"):
                    st.session_state.answered = True
                    st.session_state.user_choice = opt
                    st.rerun()
        else:
            if st.session_state.user_choice == correct_ans:
                st.success("✨ 答對了！你已掌握此知識點。")
                if st.button("解鎖下一個知識點 ➡️"):
                    st.session_state.chapter_progress[curr_ch] += 1
                    st.session_state.answered = False
                    st.rerun()
            else:
                st.error(f"❌ 答錯囉，正確答案是 {correct_ans}。再讀一次講義吧！")
                if st.button("重新嘗試"):
                    st.session_state.answered = False
                    st.rerun()
    else:
        st.balloons()
        st.success(f"🎊 恭喜！你已完成 {curr_ch} 的所有學習內容！")
        if st.button("返回選擇其他章節"):
            del st.session_state.chapter_progress[curr_ch]
            st.rerun()

# 7. 純測驗模式 (隨機抽題)
else:
    if st.button("⬅️ 返回主選單"):
        st.session_state.mode = "HOME"
        st.rerun()
    st.write("純測驗模式開發中... (可套用之前的隨機邏輯)")
    

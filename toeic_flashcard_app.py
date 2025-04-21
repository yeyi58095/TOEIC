import streamlit as st
import random
import os

def load_flashcards(file="flashcards.txt"):
    flashcards = {}
    current_unit = None
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                current_unit = line[1:-1]
                flashcards[current_unit] = {}
            elif ": " in line and current_unit:
                word, meaning = line.split(": ", 1)
                flashcards[current_unit][word.strip()] = meaning.strip()
    return flashcards

def save_wrong(word, meaning):
    with open("wrongs.txt", "a", encoding="utf-8") as f:
        f.write(f"{word}: {meaning}\n")

st.set_page_config(page_title="TOEIC 自我測驗", page_icon="📘")
st.title("📝 TOEIC 單字自我測驗")

# 載入資料
flashcards = load_flashcards()
all_units = list(flashcards.keys())

# 選單
unit = st.selectbox("📚 選擇單元", all_units)

if "deck" not in st.session_state or st.session_state.get("unit") != unit:
    st.session_state.unit = unit
    st.session_state.deck = list(flashcards[unit].items())
    random.shuffle(st.session_state.deck)
    st.session_state.index = 0
    st.session_state.show_answer = False

if st.session_state.index < len(st.session_state.deck):
    word, meaning = st.session_state.deck[st.session_state.index]
    st.markdown(f"### 🔤 單字：**{word}**")

    if not st.session_state.show_answer:
        if st.button("👀 顯示解釋"):
            st.session_state.show_answer = True
    else:
        st.markdown(f"📖 解釋：**{meaning}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✔️ 我答對了"):
                st.session_state.index += 1
                st.session_state.show_answer = False
        with col2:
            if st.button("❌ 我猜錯了"):
                save_wrong(word, meaning)
                st.session_state.index += 1
                st.session_state.show_answer = False
else:
    st.success("✅ 恭喜你完成所有單字了！")
    if st.button("🔁 再次複習此單元"):
        st.session_state.deck = list(flashcards[unit].items())
        random.shuffle(st.session_state.deck)
        st.session_state.index = 0
        st.session_state.show_answer = False

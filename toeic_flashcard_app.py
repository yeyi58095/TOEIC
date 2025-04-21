import streamlit as st
import random
import os

def load_flashcards(file="flashcards.txt"):
    flashcards = {}
    current_unit = None
    path = os.path.join(os.path.dirname(__file__), file)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
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

def run_quiz(cards):
    st.header("📘 TOEIC 單字自我檢查")

    if "idx" not in st.session_state:
        st.session_state.idx = 0
        st.session_state.deck = list(cards.items())
        random.shuffle(st.session_state.deck)
        st.session_state.show_answer = False
        st.session_state.history = []

    # 顯示題目
    if st.session_state.idx < len(st.session_state.deck):
        word, meaning = st.session_state.deck[st.session_state.idx]
        st.markdown(f"### 🔤 單字：**{word}**")

        if not st.session_state.show_answer:
            if st.button("👀 顯示解釋"):
                st.session_state.show_answer = True
                st.rerun()
            st.stop()

        # 顯示解釋與選項
        st.markdown(f"📖 解釋：**{meaning}**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✔️ 有猜對 (o)"):
                st.session_state.idx += 1
                st.session_state.show_answer = False
                st.rerun()
        with col2:
            if st.button("❌ 猜錯了 (x)"):
                save_wrong(word, meaning)
                st.session_state.history.append((word, meaning))
                st.session_state.idx += 1
                st.session_state.show_answer = False
                st.rerun()
    else:
        st.success("🎉 測驗完成！")
        if st.session_state.history:
            st.write("你答錯的單字：")
            for w, m in st.session_state.history:
                st.write(f"- {w}: {m}")
        if st.button("🔁 重新開始"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def main():
    st.set_page_config(page_title="TOEIC Flashcard", layout="centered")
    flashcards = load_flashcards()
    all_cards = {}
    for unit in flashcards:
        all_cards.update(flashcards[unit])
    run_quiz(all_cards)

if __name__ == "__main__":
    main()

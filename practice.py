import random



def load_flashcards(filename="flashcards.txt"):
    flashcards = {}
    current_unit = None

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("[") and line.endswith("]"):
                    current_unit = line[1:-1]
                    flashcards[current_unit] = {}
                elif current_unit and ": " in line:
                    word, meaning = line.split(": ", 1)
                    flashcards[current_unit][word.strip()] = meaning.strip()
    except FileNotFoundError:
        print("❌ 找不到 flashcards.txt")
    return flashcards

def list_units(flashcards):
    units = list(flashcards.keys())
    print("\n📘 可用單元：")
    for i, unit in enumerate(units, 1):
        print(f"{i}. {unit}")
    return units

def review_wrongs(wrongs_file="wrongs.txt"):
    try:
        with open(wrongs_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("⚠️ 找不到 wrongs.txt，目前沒有錯誤記錄。")
        input("按 Enter 返回主選單...")
        return

    items = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("==="):
            continue
        if ": " in line:
            word, meaning = line.split(": ", 1)
            items.append((word.strip(), meaning.strip()))

    if not items:
        print("✅ 沒有可複習的錯誤單字，太強了！")
        input("按 Enter 返回主選單...")
        return

    print("\n🛠️  複習錯誤單字模式")
    print("顯示英文 ➜ 輸入 y/n 或 o/x ➜ 顯示中文 ➜ 自動跳下一題\n")

    random.shuffle(items)
    new_wrongs = []

    for word, meaning in items:
        print(f"🔤 單字：{word}")
        ans = input("✅ 是否認得？(y/n 或 o/x): ").strip().lower()
        print(f"📖 解釋：{meaning}")
        if ans in ['n', 'x']:
            new_wrongs.append((word, meaning))
        print()

    # 覆蓋原本的 wrongs.txt 只留下最新錯的
    with open(wrongs_file, "w", encoding="utf-8") as f:
        if new_wrongs:
            f.write("=== 錯誤紀錄（複習後） ===\n")
            for w, m in new_wrongs:
                f.write(f"{w}: {m}\n")
            print(f"❌ 還有 {len(new_wrongs)} 筆不熟單字，已更新 wrongs.txt")
        else:
            print("🎉 這次全都認得了，恭喜清空錯誤清單！")

    input("\n按 Enter 返回主選單...")


def review_mode(unit_data):
    items = list(unit_data.items())
    random.shuffle(items)
    wrongs = []

    print("\n📝 TOEIC 自評模式：")
    print("顯示英文 ➜ 輸入 y/n 或 o/x ➜ 顯示中文 ➜ 自動跳下一題\n")

    for word, meaning in items:
        print(f"🔤 單字：{word}")
        ans = input("✅ 是否認得？(y/n 或 o/x): ").strip().lower()
        print(f"📖 解釋：{meaning}")
        if ans in ['n', 'x']:
            wrongs.append((word, meaning))
        print()  # 空行隔開

    if wrongs:
        with open("wrongs.txt", "a", encoding="utf-8") as f:
            f.write("\n=== 錯誤紀錄 ===\n")
            for w, m in wrongs:
                f.write(f"{w}: {m}\n")
        print(f"❌ 已記錄 {len(wrongs)} 個錯誤到 wrongs.txt")
    else:
        print("🎉 太強啦！全都認得！")

    input("\n按 Enter 返回主選單...")

def main():
    flashcards = load_flashcards()
    if not flashcards:
        return

    while True:
        print("\n📋 主選單")
        print("1. 選擇單元開始複習")
        print("2. 離開")
        print("3. 複習錯誤單字")  # 新增
        choice = input("請選擇 (1/2/3): ").strip()

        if choice == "1":
            units = list_units(flashcards)
            unit_choice = input("\n請輸入單元編號: ").strip()
            if unit_choice.isdigit():
                idx = int(unit_choice) - 1
                if 0 <= idx < len(units):
                    unit_name = units[idx]
                    review_mode(flashcards[unit_name])
                else:
                    print("❗ 單元不存在")
            else:
                print("❗ 請輸入數字")
        elif choice == "2":
            print("👋 再見！")
            break
        elif choice == "3":
            review_wrongs()  # 呼叫新功能
        else:
            print("❗ 輸入錯誤，請重新輸入")

if __name__ == "__main__":
    main()

import customtkinter as ctk
from tkinter import filedialog, messagebox
import re

def update_existing_codes(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # 빈 줄 연속 오류 수정
    compressed_lines = []
    empty_streak = False
    error_count = 0  # 수정된 오류 줄 수 세기

    for line in lines:
        if line.strip() == "":
            if not empty_streak:
                compressed_lines.append("")
                empty_streak = True
            else:
                error_count += 1  # 두 번째 이상 빈 줄은 오류로 간주
        else:
            compressed_lines.append(line)
            empty_streak = False

    code_pattern = re.compile("(BS|AD)\\d{4}")
    
    updated_lines = []
    last_bs_number = None
    last_ad_number = None
    current_bs_number = None
    current_ad_number = None

    for line in compressed_lines:
        if line.strip() == "":
            updated_lines.append("")
            last_bs_number = current_bs_number
            last_ad_number = current_ad_number
            current_bs_number = None
            current_ad_number = None
            continue

        if code_pattern.match(line.strip().split(",")[0]):
            prefix = line[:2]
            if prefix == "BS":
                if current_bs_number is None:
                    current_bs_number = (last_bs_number + 1) if last_bs_number is not None else 0
                new_code = f"BS{str(current_bs_number).zfill(4)}"
                new_line = new_code + line[6:]
                updated_lines.append(new_line)
            elif prefix == "AD":
                if current_ad_number is None:
                    current_ad_number = (last_ad_number + 1) if last_ad_number is not None else 0
                new_code = f"AD{str(current_ad_number).zfill(4)}"
                new_line = new_code + line[6:]
                updated_lines.append(new_line)
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(updated_lines))
    
    message = f"파일이 업데이트되었습니다: {filepath}"
    if error_count > 0:
        message += f"\n\n오류 {error_count}개 자동 수정됨 (빈 줄 중복 제거)."
    
    messagebox.showinfo("완료", message)


def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("TAB files", "*.tab")])
    if filepath:
        entry_file.delete(0, "end")
        entry_file.insert(0, filepath)

def run_update():
    filepath = entry_file.get()
    if filepath:
        update_existing_codes(filepath)

def clear_entry():
    entry_file.delete(0, "end")


# 🌙 Appearance and Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# 🪟 Window Setup
root = ctk.CTk()
root.title("BS, AD 코드 자동 정리기")
root.geometry("720x150")
root.resizable(True, True)

# 📦 Frame
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# 📁 Label + Entry + Buttons
label_file = ctk.CTkLabel(frame, text="파일 선택:")
label_file.grid(row=0, column=0, sticky="w", pady=5)

entry_file = ctk.CTkEntry(frame, width=400)
entry_file.grid(row=0, column=1, pady=5, padx=5)

btn_browse = ctk.CTkButton(frame, text="찾아보기", command=browse_file, width=100)
btn_browse.grid(row=0, column=2, padx=5, pady=5)

btn_clear = ctk.CTkButton(frame, text="지우기", command=clear_entry, width=80)
btn_clear.grid(row=0, column=3, padx=5, pady=5)

btn_run = ctk.CTkButton(frame, text="변환 실행", command=run_update, width=150)
btn_run.grid(row=1, column=1, pady=10, columnspan=2)

# 🚀 Start GUI
root.mainloop()

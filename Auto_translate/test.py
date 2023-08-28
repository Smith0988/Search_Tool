import tkinter as tk
from tkinter import font

def display_text_with_style(result_textbox, vietnamese_text, english_text, style_list):
    custom_font = font.Font(size=13)
    result_textbox.delete(1.0, tk.END)
    result_textbox.configure(font=custom_font)

    # Duyệt qua từng phần tử trong danh sách tiếng Anh và tiếng Việt
    for i in range(len(english_text)):
        if i in style_list:
            # In đậm
            result_textbox.insert(tk.END, english_text[i] + " ", ("bold",))
        else:
            # In nghiêng
            result_textbox.insert(tk.END, english_text[i] + " ", ("italic",))

    # Thêm ký tự xuống dòng sau tiếng Anh
    result_textbox.insert(tk.END, "\n")

    for j in range(len(vietnamese_text)):
        if j in style_list:
            # In đậm
            result_textbox.insert(tk.END, vietnamese_text[j] + " ", ("bold",))
        else:
            # In nghiêng
            result_textbox.insert(tk.END, vietnamese_text[j] + " ", ("italic",))

# Tạo một cửa sổ tkinter
window = tk.Tk()
window.geometry("400x400")

# Tạo một Text widget
result_textbox = tk.Text(window, wrap=tk.WORD)
result_textbox.pack()

# Danh sách mẫu tiếng Việt và tiếng Anh
vietnamese_text = ["Đoạn tiếng Việt 1", "Đoạn tiếng Việt 2", "Đoạn 5"]
english_text = ["English text 1", "English text 2", "Đoạn 6"]

# Danh sách chỉ định định dạng cho tiếng Anh và tiếng Việt
style_list = [0, 1]  # Để in đậm cho phần tử 0 và in nghiêng cho phần tử 1

# Định dạng in đậm và in nghiêng
result_textbox.tag_configure("bold", font=("Helvetica", 13, "bold"))
result_textbox.tag_configure("italic", font=("Helvetica", 13, "italic"))

# Gọi hàm display_text_with_style để hiển thị đoạn văn bản
display_text_with_style(result_textbox, vietnamese_text, english_text, style_list)

# Khởi chạy giao diện
window.mainloop()

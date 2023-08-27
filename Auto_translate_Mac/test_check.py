import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("Hyperlink Demo")

# Tạo một Text widget với định dạng HTML
result_textbox = scrolledtext.ScrolledText(root)
result_textbox.pack()

english_content = ["English Link 1", "English Link 2"]
english_link_list = ["http://example.com/english1", "http://example.com/english2"]

vietnamese_text = ["Vietnamese Link 1", "Vietnamese Link 2"]
vietnam_link = ["http://example.com/vietnamese1", "http://example.com/vietnamese2"]

# Duyệt qua danh sách hyperlink tiếng Anh và thêm chúng vào Text widget
for i in range(len(english_content)):
    hyperlink_html = f'<a href="{english_link_list[i]}">{english_content[i]}</a>\n'
    result_textbox.insert(tk.END, hyperlink_html, "hyperlink")

# Duyệt qua danh sách hyperlink tiếng Việt và thêm chúng vào Text widget
for i in range(len(vietnamese_text)):
    hyperlink_html = f'<a href="{vietnam_link[i]}">{vietnamese_text[i]}</a>\n'
    result_textbox.insert(tk.END, hyperlink_html, "hyperlink")

result_textbox.config(state=tk.DISABLED)  # Khóa Text widget để không cho người dùng chỉnh sửa

root.mainloop()

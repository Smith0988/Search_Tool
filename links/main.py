import tkinter as tk
from tkinter import messagebox
from tkinter import font

def search_action():
    file_name = "bb.txt"
    content = "abc xyz jkwbgorb"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    search_text = search_entry.get()
    if not search_text:
        messagebox.showwarning("Warning", "Please input search text.")
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Search Result: " + search_text)
        update_label.config(text="")

def update_action():
    content = "abc xyz"
    file_name = "aa.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    update_label.config(text="Update Successful")
    result_text.delete(1.0, tk.END)

root = tk.Tk()
window_width = 800
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

button_width = 30
entry_width = 100

# Tạo font in đậm
bold_font = font.Font(weight="bold")


search_label = tk.Label(root, text="INPUT SEARCH LINK:")
search_label.pack()

search_entry = tk.Entry(root, width=entry_width)
search_entry.pack()

search_button = tk.Button(root, text="Search", width=button_width, command=search_action, font=bold_font)
search_button.pack()

update_button = tk.Button(root, text="Update", width=button_width, command=update_action, font=bold_font)
update_button.pack()

result_text = tk.Text(root, height=5, width=80)
result_text.pack()

update_label = tk.Label(root, text="", font=bold_font)
update_label.pack()
title_font = font.Font(weight="bold")
root.title("SEARCH VIETNAMESE LINK")
root.option_add("*TLabel*Font", title_font)
root.mainloop()

import tkinter as tk
from tkinter import messagebox
from tkinter import font
from update_link import *
from find_link import *

def update_action():
    get_new_link_vn(article_url_GCT)
    get_new_link_en(file_new_gct_vn)
    add_link_to_csv(file_new_gct_en, file_new_gct_vn)

    update_label.config(text="Update Successful")
    result_text_content.delete(1.0, tk.END)
    result_text_links.delete(1.0, tk.END)

def search_action():
    search_text = search_entry.get().strip()
    if not search_text:
        messagebox.showwarning("Warning", "Please input search text.")
    else:
        # Tách dữ liệu nhập thành các phần tử riêng lẻ bằng dấu phẩy
        search_items = search_text.split(',')

        # Loại bỏ khoảng trắng ở đầu và cuối của mỗi phần tử
        search_items = [item.strip() for item in search_items]

        if len(search_items) >= 2:
            english_content, rearch_link = find_vietnamese_link(search_items[0])
            if english_content:
                result_text_content.delete(1.0, tk.END)
                result_text_content.insert(tk.END, "\n".join(english_content))
                result_text_links.delete(1.0, tk.END)
                result_text_links.insert(tk.END, "\n".join(rearch_link))
            else:
                english_text = "Have no related link in article"
                vietnamese_text = "Can not find any link"
                result_text_content.delete(1.0, tk.END)
                result_text_content.insert(tk.END, english_text)
                result_text_links.delete(1.0, tk.END)
                result_text_links.insert(tk.END, vietnamese_text)

        else:
            vietnamese_link = find_vietnamese_link_1(search_text)
            if vietnamese_link:
                result_text_content.delete(1.0, tk.END)
                result_text_content.insert(tk.END, "Input Link: " + search_text)
                result_text_links.delete(1.0, tk.END)
                result_text_links.insert(tk.END, "Result Link: "+vietnamese_link)
            else:
                vietnamese_text = "Can not find any link"
                result_text_content.delete(1.0, tk.END)
                result_text_content.insert(tk.END, "Input Link: " + search_text)
                result_text_links.delete(1.0, tk.END)
                result_text_links.insert(tk.END, "Result Link: "+ vietnamese_text)



        update_label.config(text="")

root = tk.Tk()
window_width = 1000
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

button_width = 15
entry_width = 100

# Tạo font in đậm
bold_font = font.Font(weight="bold")

# Khung hiển thị thông tin nhập vào
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

search_label = tk.Label(input_frame, text="INPUT SEARCH LINK:")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(input_frame, width=entry_width)
search_entry.pack(side=tk.LEFT)

search_button = tk.Button(input_frame, text="Search", width=button_width, command=search_action, font=bold_font)
search_button.pack(side=tk.LEFT)

# Khung hiển thị kết quả tìm kiếm
result_frame = tk.Frame(root)
result_frame.pack()

result_label_content = tk.Label(result_frame, text="Search Result (Content):", font=bold_font)
result_label_content.pack()

result_text_content = tk.Text(result_frame, height=13, width=80)
result_text_content.pack()

result_label_links = tk.Label(result_frame, text="Search Result (Links):", font=bold_font)
result_label_links.pack()

result_text_links = tk.Text(result_frame, height=13, width=80)
result_text_links.pack()

update_button = tk.Button(root, text="Update", width=button_width, command=update_action, font=bold_font)
update_button.pack(pady=10)

update_label = tk.Label(root, text="", font=bold_font)
update_label.pack()

title_font = font.Font(weight="bold")
root.title("SEARCH VIETNAMESE LINK")
root.option_add("*TLabel*Font", title_font)
root.mainloop()


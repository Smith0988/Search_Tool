import time
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from update_link import *
from write_to_world import *


waiting_text = "please wait, under processing..."

# Hàm thực hiện hành động khi người dùng chọn từ danh sách
def search_main_article_link(english_link):
    vietnamese_link = find_vietnamese_link_1(english_link)
    return vietnamese_link
def search_article_related_link(english_link):
    result_text = []
    title = get_en_article_title(english_link)
    english_content, rearch_link, english_link_list = find_vietnamese_link(english_link)
    if english_content:
        for i in range(len(english_content)):
            result_text.append(english_content[i])
            result_text.append(rearch_link[i])
        end_text = write_related_link_to_doc_1(english_content, rearch_link, english_link_list, title)
        end_text_1 = "Related hyperlink is writen on below file" + "\n" + end_text
        result_text.append(end_text_1)
        result_text_final = "\n".join(result_text)
    else:
        result_text_final = "Have no related link in article"

    return result_text_final

def update_new_link():
    get_new_link_vn(article_url_GCT)
    get_new_link_en(file_new_gct_vn)
    add_link_to_csv(file_new_gct_en, file_new_gct_vn)
    text= "Update Successful"
    return text

def create_docx_file(url):
    title, link_en, link_cn = write_en_article_to_doc(url)
    article_title = title + '.docx'
    doc = Document(article_title)
    doc.save(article_title)

    #Lấy đường dẫn
    project_folder = os.getcwd()
    # Mở tài liệu Word từ thư mục của dự án
    document_path = os.path.join(project_folder, article_title)
    result_text = "Doc file is created, please check following file: " + "\n" + document_path
    if title:
        return result_text
    else:
        return "Please check article link or network connection:"

def Auto_Translate(url):
    title, check_done = read_paragraph_in_word(url)
    article_title = title + '_translate.docx'
    project_folder = os.getcwd()
    # Mở tài liệu Word từ thư mục của dự án
    document_path = os.path.join(project_folder, article_title)
    result_text = "Translate done, please check following file: " + "\n" + document_path
    if check_done:
        return result_text
    else:
        return "Translate error, please check network or article link"

def text_execute(english, vietnam, in_text):
    count = []
    english_list =  tokenize_sentences_with_name_prefix(english)
    vietnamse_list = tokenize_sentences_with_name_prefix(vietnam)
    #print(english_list)
    #print(vietnamse_list)
    #print(in_text)
    for i in range(len(english_list)):
        check_point = False
        for j in range(len(in_text)):
            if in_text[j] in english_list[i]:
                check_point = True
                break
        if check_point:
            count.append(i)
    return english_list, vietnamse_list, count

def update_link():
    update_text = update_new_link()
    display_result(update_text)

def search_main_link():
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    else:
        display_result(waiting_text)
        result = search_main_article_link(user_input)
        display_result(result)


def search_related_link():
    # Xóa nội dung hiển thị kết quả
    pattern = r"^(http:|https:).*\.html$"
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    elif not re.match(pattern, user_input):
            messagebox.showwarning("Warning", "Please input correct link.")
    else:
        #custom_font = font.Font(family="Arial", size=16)
        display_result(waiting_text)
        result = search_article_related_link(user_input)
        display_result(result)

def article_content():
    # Xóa nội dung hiển thị kết quả
    pattern = r"^(http:|https:).*\.html$"
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    elif not re.match(pattern, user_input):
            messagebox.showwarning("Warning", "Please input correct link.")
    else:
        result = create_docx_file(user_input)
        display_result(result)

def translation():
    # Xóa nội dung hiển thị kết quả
    pattern = r"^(http:|https:).*\.html$"
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    elif not re.match(pattern, user_input):
            messagebox.showwarning("Warning", "Please input correct link.")
    else:
        result = Auto_Translate(user_input)
        display_result(result)


def searc_kv():
    user_input = input_text.get().strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    else:
        result_textbox.delete(1.0, tk.END)
        result_textbox.configure(font=custom_font)
        result_textbox.tag_configure("bold", font=("Helvetica", 11, "bold"))
        result_textbox.tag_configure("italic", font=("Helvetica", 11, "italic"))
        english_text_in, vietname_text_in, in_text = find_translation(user_input)
        if not english_text_in:
            result_textbox.insert(tk.END, "Can not found, please check input text")
            return
        for h in range(len(english_text_in)):
            english_text, vietname_text, list = text_execute(english_text_in[h], vietname_text_in[h], in_text)
            for i in range(len(english_text)):
                if i in list:
                    result_textbox.insert(tk.END, english_text[i] + " ", ("bold",))
                else:
                    result_textbox.insert(tk.END, english_text[i] + " ", ("italic",))
            result_textbox.insert(tk.END, "\n")
            result_textbox.insert(tk.END, "================================================================================")
            result_textbox.insert(tk.END, "\n")
            for j in range(len(vietname_text)):
                if j in list:
                    result_textbox.insert(tk.END, vietname_text[j] + " ", ("bold",))
                else:
                    result_textbox.insert(tk.END, vietname_text[j] + " ", ("italic",))
            result_textbox.insert(tk.END, "\n")
            result_textbox.insert(tk.END, "================================================================================")
            result_textbox.insert(tk.END, "\n")

def clear_text():
    input_text.delete(0, "end")  # Xóa nội dung từ đầu đến cuối của trường văn bản

def copy_text():
    result_text = result_textbox.get("1.0", tk.END)  # Lấy nội dung từ dòng 1, ký tự 0 đến cuối
    root.clipboard_clear()  # Xóa clipboard hiện có
    root.clipboard_append(result_text)  # Đặt nội dung vào clipboard

def display_result(result_text):
    custom_font = font.Font(size=13)
    result_textbox.delete(1.0, tk.END)
    result_textbox.configure(font=custom_font)
    result_textbox.insert(tk.END, result_text)

root = tk.Tk()
window_width = 1300
window_height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
# Tạo 6 cột và cho phép co giãn
# Tạo 6 cột và cho phép co giãn
for i in range(6):
    root.grid_columnconfigure(i, weight=1)

# Tạo 4 hàng và cho phép co giãn
for i in range(6):
    root.grid_rowconfigure(i, weight=1)

# Tạo các widget hoặc frame con và đặt chúng trong các cell của grid
for i in range(6):
    for j in range(6):
        frame = tk.Frame(root, bg="#FAF0E6")
        frame.grid(row=i, column=j, sticky='nsew')

button_width = 10
button_width_1 = 8
entry_width = 100 # Đặt giá trị chiều rộng cho Entry widget

# Tạo font in đậm
button_font = font.Font(weight="bold")
# Hàng 1
action_button_1 = tk.Button(root, text="Update New", width=button_width, height=1, command=update_link,bg="#00405d", fg="white",font=button_font)
action_button_1.grid(row=0, column=0, padx=(10, 0), pady=10, sticky='w')

action_button_2 = tk.Button(root, text="Main Link", width=button_width, height=1, command=search_main_link,bg="#00405d", fg="white",font=button_font)
action_button_2.grid(row=0, column=0, padx=(190, 0), pady=10, sticky='w')

action_button_3 = tk.Button(root, text="Related Link", width=button_width, height=1, command=search_related_link,bg="#00405d", fg="white",font=button_font)
action_button_3.grid(row=0, column=0, padx=(380, 0), pady=10, sticky='w')

action_button_4 = tk.Button(root, text="A_Content", width=button_width, height=1, command=article_content,bg="#00405d", fg="white",font=button_font)
action_button_4.grid(row=0, column=0, padx=(570, 0), pady=10, sticky='w')

action_button_5 = tk.Button(root, text="KV_Search", width=button_width, height=1, command=searc_kv,bg="#00405d", fg="white",font=button_font)
action_button_5.grid(row=0, column=0, padx=(760, 0), pady=10, sticky='w')

action_button_6 = tk.Button(root, text="Auto_Trans", width=button_width, height=1, command=translation,bg="#00405d", fg="white",font=button_font)
action_button_6.grid(row=0, column=0, padx=(950, 0), pady=10, sticky='w')


# Hàng 2
label_font = font.Font(family="Helvetica", size=15)
# Tạo Label widget và sử dụng font đã chỉ định
input_label = tk.Label(root, text="Search Text", font=label_font, bg="white", fg="black")
input_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky='w')

# Tạo một font với chiều cao mong muốn
custom_font = font.nametofont("TkDefaultFont")
custom_font.configure(size=15)  # Thay đổi size để điều chỉnh chiều cao

# Tạo một tk.Entry và sử dụng font đã chỉ định
input_text = tk.Entry(root, width=entry_width, font=custom_font)
input_text.grid(row=1, column=0, padx=(150, 0), pady=0, sticky='w')

# Tạo một nút "Clear" để xóa nội dung trường văn bản
button_font = font.Font(family="Helvetica", size=13)
clear_button = tk.Button(root, text="Clr", width=6, height=1, command=clear_text, font=button_font, bg="white", fg="black")
clear_button.grid(row=1, column=4, padx=(0, 0), pady=0, sticky='w')


# Tạo Label widget và sử dụng font đã chỉ định
result_label = tk.Label(root, text="Result text", font=label_font, bg="white", fg="black")
result_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky='w')

# Tạo nút "Copy" để sao chép nội dung từ vùng văn bản đa dòng
copy_button = tk.Button(root, text="Copy text result", width=20, height=1, command=copy_text, font=button_font, bg="white", fg="black")
copy_button.grid(row=2, column=0, padx=(150, 0), pady=0, sticky='w')

# Tạo thanh cuộn cho Text widget
result_textbox = tk.Text(root, height=18, width=130)
result_textbox.grid(row=3, column=0, columnspan=5, padx=(10, 0), pady=0, sticky='snew')

# Tạo thanh cuộn
scrollbar = tk.Scrollbar(root, orient="vertical", command=result_textbox.yview)
scrollbar.grid(row=3, column=5, sticky="snw")
result_textbox.config(yscrollcommand=scrollbar.set)


title_font = font.Font(family="Helvetica", size=20, weight="bold")  # Điều chỉnh family, size, và weight theo mong muốn
root.title("SEARCHING TOOL")
root.option_add("*TLabel*Font", title_font)
root.option_add("*TLabel*Foreground", "blue")  # Đổi màu chữ của title thành màu xanh

root.mainloop()


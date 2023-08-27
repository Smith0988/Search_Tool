import tkinter as tk
from tkinter import messagebox
from tkinter import font
from update_link import *
from write_to_world import *


waiting_text = "please wait, under processing..."

# Hàm thực hiện hành động khi người dùng chọn từ danh sách
def search_main_link(english_link):
    vietnamese_link = find_vietnamese_link_1(english_link)
    return vietnamese_link
def search_related_link(english_link):
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

def perform_action():
    # Xóa nội dung hiển thị kết quả
    selected_action = action_var.get()
    user_input = input_text.get().strip()
    if selected_action == "Please select action...":
        messagebox.showwarning("Warning", "Please select one item on crop_down.")
    elif selected_action == "Update Link":
        update_text = update_new_link()
        display_result(update_text)
    elif not user_input:
        messagebox.showwarning("Warning", "Please input search text.")
    else:
        #custom_font = font.Font(family="Arial", size=16)
        custom_font = font.Font(size=16)
        result_textbox.delete(1.0, tk.END)
        result_textbox.configure(font=custom_font)
        result_textbox.insert(tk.END, waiting_text)
        # Gọi hàm thực hiện hành động sau một khoảng thời gian ngắn (ví dụ: 100ms)
        root.after(200, execute_selected_action)

def execute_selected_action():
    selected_action = action_var.get()
    user_input = input_text.get().strip()
    pattern = r"^(http:|https:).*\.html$"
    if selected_action == "Search main article link":
        result = search_main_link(user_input)
        display_result(result)
    elif selected_action == "Search related link":
        if re.match(pattern, user_input):
            result = search_related_link(user_input)
            display_result(result)
        else:
            messagebox.showwarning("Warning", "Please input correct link.")
    elif selected_action == "Create docx file":
        if re.match(pattern, user_input):
            result = create_docx_file(user_input)
            display_result(result)
        else:
            messagebox.showwarning("Warning", "Please input correct link.")
    elif selected_action == "Auto_Translate":
        if re.match(pattern, user_input):
            result = Auto_Translate(user_input)
            display_result(result)
        else:
            messagebox.showwarning("Warning", "Please input correct link.")


    # Đánh dấu rằng nút "Run" đã được nhấn
    run_button_pressed = True

# Hàm hiển thị kết quả trong cửa sổ kết quả
def display_result(result_text):
    custom_font = font.Font(size=13)
    result_textbox.delete(1.0, tk.END)
    result_textbox.configure(font=custom_font)
    result_textbox.insert(tk.END, result_text)

root = tk.Tk()
window_width = 1200
window_height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

button_width = 10
entry_width = 80 # Đặt giá trị chiều rộng cho Entry widget

# Tạo font in đậm
bold_font = font.Font(weight="bold")

# Hàng 1
action_button = tk.Button(root, text="Run", width=button_width, height=1, command=perform_action)
action_button.grid(row=0, column=0, padx=(10, 0), pady=20, sticky='w')

# Tạo danh sách thả xuống cho các hành động
action_var = tk.StringVar(root)
action_var.set("Please select action...")  # Đặt hành động mặc định
action_dropdown = tk.OptionMenu(root, action_var, "Update Link", "Search main article link", "Search related link", "Create docx file", "Auto_Translate", "-----")
action_dropdown.grid(row=0, column=1, padx=(0, 10), pady=20, sticky='w')

# Hàng 2
input_label = tk.Label(root, text="Search Text:")
input_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky='w')

# Tạo một font với chiều cao mong muốn
custom_font = font.nametofont("TkDefaultFont")
custom_font.configure(size=15)  # Thay đổi size để điều chỉnh chiều cao

# Tạo một tk.Entry và sử dụng font đã chỉ định
input_text = tk.Entry(root, width=entry_width, font=custom_font)
input_text.grid(row=1, column=1, padx=(0, 10), pady=10, sticky='w')

# Hàng 3
result_label = tk.Label(root, text="Search Result:")
result_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky='w')

# Tạo thanh cuộn cho Text widget
result_textbox = tk.Text(root, height=18, width=130)
result_textbox.grid(row=3, column=0, columnspan=2, padx=(10, 10), pady=10, sticky='w')

# Tạo thanh cuộn
scrollbar = tk.Scrollbar(root, orient="vertical", command=result_textbox.yview)
scrollbar.grid(row=3, column=2, sticky="ns")
result_textbox.config(yscrollcommand=scrollbar.set)


title_font = font.Font(family="Helvetica", size=20, weight="bold")  # Điều chỉnh family, size, và weight theo mong muốn
root.title("SEARCHING TOOL")
root.option_add("*TLabel*Font", title_font)
root.mainloop()


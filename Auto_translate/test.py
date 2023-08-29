import tkinter as tk

# Hàm để sao chép title và hyperlink vào clipboard
def copy_title_and_hyperlink():
    title = "Người đàn ông 70 tuổi ở Hà Bắc bị giam giữ vì phân phát tài liệu thông tin Pháp Luân Công"
    hyperlink = "https://vn.minghui.org/news/251544-nguoi-dan-ong-70-tuoi-o-ha-bac-bi-giam-giu-vi-phan-phat-tai-lieu-thong-tin-phap-luan-cong.html"

    # Kết hợp title và hyperlink
    title_with_hyperlink = f"<a href=\"{hyperlink}\">{title}</a>"

    # Sao chép vào clipboard
    root.clipboard_clear()
    root.clipboard_append(title_with_hyperlink)

# Tạo cửa sổ tkinter
root = tk.Tk()

# Tạo label để hiển thị title với hyperlink
title_label = tk.Label(root, text="Người đàn ông 70 tuổi ở Hà Bắc bị giam giữ vì phân phát tài liệu thông tin Pháp Luân Công", fg="blue", cursor="hand2")
title_label.pack()

# Định nghĩa hyperlink
hyperlink = "https://vn.minghui.org/news/251544-nguoi-dan-ong-70-tuoi-o-ha-bac-bi-giam-giu-vi-phan-phat-tai-lieu-thong-tin-phap-luan-cong.html"

# Thiết lập sự kiện click cho label để mở hyperlink trong trình duyệt
def open_hyperlink(event):
    import webbrowser
    webbrowser.open_new(hyperlink)

title_label.bind("<Button-1>", open_hyperlink)

# Tạo nút "Copy" để sao chép title và hyperlink
copy_button = tk.Button(root, text="Copy", command=copy_title_and_hyperlink)
copy_button.pack()

root.mainloop()


import pandas as pd

# Đọc tệp CSV gốc
input_csv = "link_eng_vn_gct.csv"
df = pd.read_csv(input_csv, header=None, names=["English", "Vietnamese"])

# Lấy cột 1 (tiếng Anh) và ghi vào tệp văn bản
with open("links_gct_en_final.txt", "w", encoding="utf-8") as en_file:
    en_links = df["English"].tolist()
    for link in en_links:
        en_file.write(link + "\n")

# Lấy cột 2 (tiếng Việt) và ghi vào tệp văn bản
with open("links_gct_vn_final.txt", "w", encoding="utf-8") as vn_file:
    vn_links = df["Vietnamese"].tolist()
    for link in vn_links:
        vn_file.write(link + "\n")

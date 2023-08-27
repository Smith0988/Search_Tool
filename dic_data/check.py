import pandas as pd

# Đọc hai tệp CSV vào DataFrame
df_link_eng_vn = pd.read_csv("link_eng_vn_gct_1.csv")
df_all_links = pd.read_csv("all_link_use.csv")

# So sánh các giá trị trong cột 1 của hai DataFrame
common_links = df_link_eng_vn[df_link_eng_vn.iloc[:, 0].isin(df_all_links.iloc[:, 0])]

# Tạo DataFrame mới từ df_link_eng_vn chỉ chứa các hàng không trùng với df_all_links
unique_links_in_link_eng_vn = df_link_eng_vn[~df_link_eng_vn.iloc[:, 0].isin(df_all_links.iloc[:, 0])]

# Ghi ra các tệp CSV tương ứng
common_links.to_csv("link_eng_vn_gct_3.csv", index=False)
unique_links_in_link_eng_vn.to_csv("link_eng_vn_gct_4.csv", index=False)

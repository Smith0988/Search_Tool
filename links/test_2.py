import pandas as pd

# Đọc tệp CSV gốc
input_csv = "link_eng_vn_gct.csv"
df = pd.read_csv(input_csv, header=None, names=["English", "Vietnamese"])

# Tạo hai DataFrame tương ứng cho việc lọc dữ liệu
df_with_minghui = df[df["English"].str.contains("en.minghui.org")]
df_without_minghui = df[~df["English"].str.contains("en.minghui.org")]

# Ghi ra các tệp CSV tương ứng
output_csv_with_minghui = "link_eng_vn_gct_1.csv"
df_with_minghui.to_csv(output_csv_with_minghui, index=False, header=False)

output_csv_without_minghui = "link_eng_vn_gct_2.csv"
df_without_minghui.to_csv(output_csv_without_minghui, index=False, header=False)

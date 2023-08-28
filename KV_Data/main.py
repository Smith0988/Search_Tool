import csv

# Đọc nội dung từ file English.txt và Vietnam.txt vào list1 và list2
with open('English.txt', 'r', encoding='utf-8') as file1, open('Vietnam.txt', 'r', encoding='utf-8') as file2:
    list1 = file1.readlines()
    list2 = file2.readlines()

# Loại bỏ các phần tử trống
list1 = [line.strip() for line in list1 if line.strip()]
list2 = [line.strip() for line in list2 if line.strip()]
# Kiểm tra độ dài của 2 list
if len(list1) == len(list2):
    # Ghi list1 và list2 vào file CSV
    with open('KV_data.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for item1, item2 in zip(list1, list2):
            writer.writerow([item1, item2])
    print("Ghi thành công vào output.csv")
else:
    print("Độ dài của hai danh sách không trùng nhau.  -----------------------")
print(len(list1))
print(len(list2))

english_text = [
    "This is the first part of the text.",
    "Bản quyền © 2023 Minghui.org. Mọi quyền được bảo lưu.",
    "This is the second part of the text.",
    "And so on..."
]

# Tìm vị trí của phần "Bản quyền © 2023 Minghui.org. Mọi quyền được bảo lưu."
split_point = english_text.index("Bản quyền © 2023 Minghui.org. Mọi quyền được bảo lưu.")

# Tách danh sách thành hai phần
list1 = english_text[:split_point]
list2 = english_text[split_point:]

# In ra hai danh sách
print("List 1:")
for item in list1:
    print(item)

print("\nList 2:")
for item in list2:
    print(item)

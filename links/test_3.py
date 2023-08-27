import re

import requests
from bs4 import BeautifulSoup

file_new_tdth_vn = "tdth_vn_new.txt"
file_new_gct_vn = "gct_vn_new.txt"
file_new_tdth_en = "tdth_en_new.txt"
file_new_gct_en = "gct_en_new.txt"



def read_number_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            number = int(file.read())
            return number
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except ValueError:
        print(f"Invalid content in '{file_path}'. It should contain a valid number.")
        return None


def write_number_to_file(file_path, number):
    try:
        with open(file_path, 'w') as file:
            file.write(str(number))
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_to_text(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)

def write_to_text_1(file_name, content):
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(content + '\n')



def write_list_to_txt(filename, lst):
    with open(filename, 'a', encoding='utf-8') as file:
        for item in lst:
            file.write(item + '\n')


def change_vn_link_to_eng(url_vn):
    if not url_vn.startswith("http://") and not url_vn.startswith("https://"):
        url_vn = "https:" + url_vn  # Thêm schema "https:" nếu cần

    response = requests.get(url_vn)
    link_fail = "Can not find English Link"

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='articleBody')

        # Lấy toàn bộ nội dung của articleBody
        article_text = article_body.get_text()

        # Tìm các chuỗi liên kết sau "Bản tiếng Anh" hoặc "Bản tiếng Anh:"
        link_matches = re.findall(r'Bản\s+tiếng\s+Anh\s*:?\s*(https?://[^\s"]+\.htm)', article_text)

        if link_matches:
            for link_match in link_matches:
                return link_match

        # Loại bỏ các đoạn trống
        non_empty_paragraphs = [p for p in article_body.find_all('p') if p.get_text(strip=True)]

        # Duyệt đoạn văn bản cuối cùng và từ dưới lên
        for paragraph in reversed(non_empty_paragraphs):
            paragraph_text = paragraph.get_text(strip=True)
            if "en.minghui.org" in paragraph_text:
                link_match = re.search(r'https?://[^\s"]+\.htm', paragraph_text)
                if link_match:
                    return link_match.group()

        # Duyệt đoạn văn bản thứ 2 từ dưới lên
        if len(non_empty_paragraphs) >= 2:
            second_last_paragraph = non_empty_paragraphs[-2].get_text(strip=True)
            link_match = re.search(r'https?://[^\s"]+\.htm', second_last_paragraph)
            if link_match:
                return link_match.group()

        return link_fail
    else:
        return link_fail


def read_links_from_file(file_name):
    links = []
    with open(file_name, 'r') as file:
        for line in file:
            link = line.strip()  # Remove leading/trailing whitespace
            links.append(link)
    return links

# File name containing the links
file_name_vn = "gct_vn_new.txt"
file_name_en = "gct_en_new.txt"
index_file_name = 'row_number.txt'


# Read links from the file
link_list = read_links_from_file(file_name_vn)
index = read_number_from_file(index_file_name)
a = 10000
for i in range(index, index + a):
    write_number_to_file(index_file_name, i+1)
    vn_link_index = link_list[i]
    en_link_index = change_vn_link_to_eng(vn_link_index)
    write_to_text_1(file_name_en, en_link_index)
    write_to_text_1("link_use_vn.txt", vn_link_index)
write_number_to_file(index_file_name, index + a)


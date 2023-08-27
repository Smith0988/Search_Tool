import csv

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

# Khai báo
file_new_tdth_vn = "tdth_vn_new.txt"
file_new_gct_vn = "gct_vn_new.txt"
file_new_tdth_en = "tdth_en_new.txt"
file_new_gct_en = "gct_en_new.txt"

file_total_tdth_vn = "links_tdth_vn_final.txt"
file_total_gct_vn = "links_gct_vn_final.txt"
file_total_tdth_en = "links_tdth_en_final.txt"
file_total_gct_en = "links_gct_en_final.txt"

file_tdth_csv = 'link_eng_vn_tdth.csv'
file_gct_csv = 'link_eng_vn_gct.csv'

# Đường dẫn link bài báo
article_url_GCT = "https://vn.minghui.org/news/category/cuoc-buc-hai-o-trung-quoc"

file_txt = 'gct_vn_new.txt'
file_csv = 'link_eng_vn_gct.csv'

def read_column_from_csv(file_name, column_index):
    df = pd.read_csv(file_name, header=None)
    column_data = df.iloc[:, column_index]
    return column_data.tolist()

def read_links_from_file_1(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
def check_links(file_txt, file_csv, column_index=1):
    with open(file_txt, 'r') as f_txt:
        l1 = [line.strip() for line in f_txt.readlines()]

    l2 = read_column_from_csv(file_csv, column_index)

    l3 = [link for link in l1 if link not in l2]

    return l3

def get_new_link_vn(url_vn):
    response = requests.get(url_vn)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='columnRel right')

        # Lấy toàn bộ nội dung trong đoạn văn bản
        all_link = []
        for link in article_body.find_all('a', href=True):
            all_link.append(link['href'])

        # Ghi danh sách link vào file text với chế độ không ghi đè

        with open(file_new_gct_vn, "w", encoding="utf-8") as file:
            for link in all_link:
                file.write(link + "\n")
        new_link = check_links(file_txt, file_csv, column_index=1)

        with open(file_new_gct_vn, "w", encoding="utf-8") as file:
            for link in new_link:
                file.write(link + "\n")
        return new_link
    else:
        return []


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
        link_matches = re.findall(r'Bản\s+tiếng\s+Anh\s*:?\s*(https?://[^\s"]+\.html)', article_text)

        if link_matches:
            for link_match in link_matches:
                return link_match

        # Loại bỏ các đoạn trống
        non_empty_paragraphs = [p for p in article_body.find_all('p') if p.get_text(strip=True)]

        # Duyệt đoạn văn bản cuối cùng và từ dưới lên
        for paragraph in reversed(non_empty_paragraphs):
            paragraph_text = paragraph.get_text(strip=True)
            if "en.minghui.org" in paragraph_text:
                link_match = re.search(r'https?://[^\s"]+\.html', paragraph_text)
                if link_match:
                    return link_match.group()

        # Duyệt đoạn văn bản thứ 2 từ dưới lên
        if len(non_empty_paragraphs) >= 2:
            second_last_paragraph = non_empty_paragraphs[-2].get_text(strip=True)
            link_match = re.search(r'https?://[^\s"]+\.html', second_last_paragraph)
            if link_match:
                return link_match.group()

        return link_fail
    else:
        return link_fail


def find_relative_link(url_vn):
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
        link_matches = re.findall(r'Bản\s+tiếng\s+Anh\s*:?\s*(https?://[^\s"]+\.html)', article_text)

        if link_matches:
            for link_match in link_matches:
                return link_match

        # Loại bỏ các đoạn trống
        non_empty_paragraphs = [p for p in article_body.find_all('p') if p.get_text(strip=True)]

        # Duyệt đoạn văn bản cuối cùng và từ dưới lên
        for paragraph in reversed(non_empty_paragraphs):
            paragraph_text = paragraph.get_text(strip=True)
            if "en.minghui.org" in paragraph_text:
                link_match = re.search(r'https?://[^\s"]+\.html', paragraph_text)
                if link_match:
                    return link_match.group()

        # Duyệt đoạn văn bản thứ 2 từ dưới lên
        if len(non_empty_paragraphs) >= 2:
            second_last_paragraph = non_empty_paragraphs[-2].get_text(strip=True)
            link_match = re.search(r'https?://[^\s"]+\.html', second_last_paragraph)
            if link_match:
                return link_match.group()

        return link_fail
    else:
        return link_fail


def get_new_link_en(file_name):
    # Mở file links.txt để đọc
    with open(file_name, "r", encoding="utf-8") as file:
        content = file.read()

    # Chuyển nội dung file thành list các link
    link_vn_new = content.splitlines()
    link_en_new = []

    # Duyệt từng phần tử trong list link_gct_vn và đổi sang link en
    for link in link_vn_new:
        link_en_new.append(change_vn_link_to_eng(link))

    # Ghi link vào file
    with open(file_new_gct_en, "w", encoding="utf-8") as file:
        for link in link_en_new:
            file.write(link + "\n")


def add_link_to_csv(file_name_en, file_name_vn):
    # Mở file links.txt để đọc
    with open(file_name_vn, "r", encoding="utf-8") as file:
        content_vn = file.read()

    with open(file_name_en, "r", encoding="utf-8") as file:
        content_en = file.read()

    # Chuyển nội dung file thành list các link
    link_vn_new = content_vn.splitlines()
    link_en_new = content_en.splitlines()

    if len(link_en_new) == len(link_vn_new) and link_en_new and link_vn_new:

        # Tạo DataFrame từ danh sách câu tiếng Anh và tiếng Việt đã tách
        df = pd.DataFrame({'English_Link': link_en_new, 'Vietnamese_Link': link_vn_new}, index=None)

        # Ghi vào file report_combined.csv mà không ghi đè dữ liệu

        df.to_csv(file_gct_csv, mode='a', header=False, index=False)

    os.remove(file_new_gct_vn)
    os.remove(file_new_gct_en)


#get_new_link_vn(article_url_GCT)
#get_new_link_en(file_new_gct_vn)
#add_link_to_csv(file_new_gct_en, file_new_gct_vn)

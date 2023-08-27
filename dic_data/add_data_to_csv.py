import csv
import pandas as pd
import nltk
import requests
from bs4 import BeautifulSoup
import re

nltk.download('punkt')  # Download data for sentence tokenizer
from nltk.tokenize import sent_tokenize


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


def write_use_link_to_csv(text1, text2):
    # Tạo DataFrame với hai cột "English" và "Vietnamese"
    df = pd.DataFrame({'English': [text1], 'Vietnamese': [text2]})

    # Ghi vào file CSV, mode='a' để ghi tiếp dữ liệu nếu file đã tồn tại
    df.to_csv('all_link_use.csv', mode='a', header=False, index=False)


def write_not_use_link_to_csv(text1, text2):
    # Tạo DataFrame với hai cột "English" và "Vietnamese"
    df = pd.DataFrame({'English': [text1], 'Vietnamese': [text2]})

    # Ghi vào file CSV, mode='a' để ghi tiếp dữ liệu nếu file đã tồn tại
    df.to_csv('link_not_use_complete.csv', mode='a', header=False, index=False)


def write_to_text(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)


def write_list_to_txt(filename, lst):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in lst:
            file.write(item + '\n')


def get_en_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_contents = soup.find('div', class_='article-body-content')

        if article_contents:
            # Tìm các phần tử con của 'articleBody'
            paragraphs = article_contents.find_all(['p', 'h3'])

            valid_paragraphs = []
            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)
                match = re.match(r'^\d+\.\s*(.*)', text)
                if match:
                    valid_paragraphs.append(match.group(1))
                else:
                    valid_paragraphs.append(text)

            # Ghi nội dung các đoạn văn bản hợp lệ vào biến article_content
            article_content = "\n".join(valid_paragraphs)
            return article_content
        else:
            return []
    else:
        return []


def get_en_article_title(url):
    try:
        # Tải nội dung của trang web
        response = requests.get(url)

        # Kiểm tra nếu yêu cầu thành công (status code 200)
        if response.status_code == 200:
            # Sử dụng BeautifulSoup để phân tích cú pháp trang web
            soup = BeautifulSoup(response.content, 'html.parser')

            # Tìm thẻ div có class là 'article-title'
            article_title_tag = soup.find('div', class_='article-title')

            # Kiểm tra nếu tồn tại thẻ và lấy nội dung text của tiêu đề
            if article_title_tag:
                article_title = article_title_tag.text.strip()
                return article_title
            else:
                return ""
        else:
            return ""
    except Exception as e:
        return ""


def get_vn_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_body = soup.find('div', class_='articleBody')
        if article_body:
            # Tìm các phần tử con của 'articleBody'
            paragraphs = article_body.find_all('p')

            # Loại bỏ nội dung của đoạn đầu tiên nếu không chứa ký tự "["
            if "[" not in paragraphs[0].get_text(strip=True):
                paragraphs = paragraphs[1:]
            valid_paragraphs = []
            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)
                match = re.match(r'^\d+\.\s*(.*)', text)
                if match:
                    valid_paragraphs.append(match.group(1))
                else:
                    valid_paragraphs.append(text)

            # Ghi nội dung các đoạn văn bản hợp lệ vào biến article_content
            article_content = "\n".join(valid_paragraphs)
            return article_content
        else:
            return []
    else:
        return []


def get_links_from_csv(file_path):
    links_en = []
    links_vn = []

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Bỏ qua header nếu có

        for row in reader:
            link_en, link_vn = row[0], row[1]
            links_en.append(link_en)
            links_vn.append(link_vn)

    return links_en, links_vn


def text_normalization_vn_f(vn_article):
    lines_vn = vn_article.split('\n')
    new_vn_list = []

    for text_vn in lines_vn:

        if "Họ và tên" in text_vn or "Ngày mất:" in text_vn or "Giới tính:" in text_vn or "Tên Trung Quốc:" in text_vn:
            continue
        if 'Họ và tên' in text_vn or 'Ngày mất' in text_vn or 'Giới tính:' in text_vn or 'Tên Trung Quốc:' in text_vn:
            continue
        if "Bản quyền © 2023" in text_vn or "(Hết)" in text_vn or "(Còn tiếp.)" in text_vn or "Bản tiếng" in text_vn or "Bản tiếng Hán" in text_vn or "Bài liên quan" in text_vn or "Thông tin liên hệ" in text_vn or "Thông tin liên lạc" in text_vn or "Các báo cáo liên quan" in text_vn or "Báo cáo liên quan" in text_vn or "Mọi bài viết, hình ảnh, hay nội dung" in text_vn or "Bài viết chỉ thể hiện quan điểm" in text_vn or "Mọi nội dung đăng trên trang" in text_vn or "danh sách những thủ phạm" in text_vn:
            break

        if 'Bản quyền © 2023' in text_vn or'(Hết)' in text_vn or '(Còn tiếp.)' in text_vn or 'Bản tiếng' in text_vn or 'Bản tiếng Hán' in text_vn or 'Bài liên quan' in text_vn or 'Thông tin liên hệ' in text_vn or 'Thông tin liên lạc' in text_vn or 'Các báo cáo liên quan' in text_vn or 'Báo cáo liên quan' in text_vn or 'Mọi bài viết, hình ảnh, hay nội dung' in text_vn or 'Bài viết chỉ thể hiện quan điểm' in text_vn or 'Mọi nội dung đăng trên trang' in text_vn or 'danh sách những thủ phạm' in text_vn:
            break

        if "[MINH HUỆ" in text_vn:
            text_vn = re.sub(r'\[.*?\]', '', text_vn)
        if text_vn.strip():
            new_vn_list.append(text_vn)

    return new_vn_list


def text_normalization_en_f(en_article):
    lines_en = en_article.split('\n')
    new_en_list = []
    for i in range(len(lines_en)):
        text_en = lines_en[i]
        if 'Related Report' in text_en or 'Related report' in text_en or 'Perpetrators’ contact information' in text_en or 'list of the perpetrators' in text_en:
            break

        if "Related Report" in text_en or "Perpetrators’ contact information" in text_en or "list of the perpetrators" in text_en:
            break

        if "Chinese Name" in text_en or "English Name" in text_en:
            continue
        if 'Chinese Name' in text_en or 'English Name' in text_en:
            continue

        if "(Minghui.org)" in text_en:
            text_en = re.sub(r'\(Minghui.org\)', '', text_en)
        if text_en.strip():
            new_en_list.append(text_en)

    return new_en_list


def tokenize_sentences_with_name_prefix(text):
    name_prefixes = ["Mr.", "Ms.", "No."]

    # Replace name prefixes with placeholders
    for prefix in name_prefixes:
        text = text.replace(prefix, f"{prefix}DOT")

    # Tokenize sentences
    sentences = nltk.sent_tokenize(text)

    # Replace the placeholders back to name prefixes
    for prefix in name_prefixes:
        sentences = [sentence.replace(f"{prefix}DOT", prefix) for sentence in sentences]

    return sentences


def paragraph_indentation(en_article, vn_article):
    new_en_list = []
    new_vn_list = []
    print("truoc chuan hoa: ")
    print(len(en_article))
    print(len(vn_article))
    index = max(len(en_article), len(vn_article)) - min(len(en_article), len(vn_article))
    print(index)
    if len(en_article) > len(vn_article):
        j = 0
        for i in range(len(vn_article)):
            en_text = en_article[i + j]
            vn_text = vn_article[i]
            english_sentences = tokenize_sentences_with_name_prefix(en_text)
            vietnamese_sentences = tokenize_sentences_with_name_prefix(vn_text)
            #english_sentences_2 = tokenize_sentences_with_name_prefix(en_article[i + j + 1])
            if j == index and (len(vietnamese_sentences) != len(english_sentences)):
                break
            if j == index:
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)
                continue
            #if (len(vietnamese_sentences) != len(english_sentences)) and (
                    #len(vietnamese_sentences) == len(english_sentences) + len(english_sentences_2)):
            if (len(vietnamese_sentences) != len(english_sentences)):
                # print("gia tri J la:  ", j)
                # print("en_text:  ", en_text)
                # print("vn_text:  ", vn_text)
                # print("Độ dài đoạn vn thứ", i + j, len(vietnamese_sentences))
                # print("Độ dài đoạn en thứ", i, len(english_sentences))
                # print("Độ dài đoạn vn thứ", i + j+1, len(tokenize_sentences_with_name_prefix(vn_article[i + j+1])))
                temp_list = en_text + " " + en_article[i + j + 1]
                new_en_list.append(temp_list)
                new_vn_list.append(vn_text)
                j = j + 1
            else:
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)

    else:
        j = 0
        for i in range(len(en_article)):
            en_text = en_article[i]
            vn_text = vn_article[i + j]
            english_sentences = tokenize_sentences_with_name_prefix(en_text)
            vietnamese_sentences = tokenize_sentences_with_name_prefix(vn_text)
            if j == index and (len(vietnamese_sentences) != len(english_sentences)):
                break
            if j == index:
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)
                continue
            #vietnamese_sentences_2 = tokenize_sentences_with_name_prefix(vn_article[i + j + 1])
            #if (len(vietnamese_sentences) != len(english_sentences)) and (
            #len(english_sentences) == len(vietnamese_sentences) + len(vietnamese_sentences_2)):

            if (len(vietnamese_sentences) != len(english_sentences)):
                # print("gia tri J la:  ", j)
                # print("en_text:  ", en_text)
                # print("vn_text:  ", vn_text)
                # print("Độ dài đoạn vn thứ", i + j, len(vietnamese_sentences))
                # print("Độ dài đoạn en thứ", i, len(english_sentences))
                # print("Độ dài đoạn vn thứ", i + j+1, len(tokenize_sentences_with_name_prefix(vn_article[i + j+1])))
                temp_list = vn_text + " " + vn_article[i + j + 1]
                new_vn_list.append(temp_list)
                new_en_list.append(en_text)
                j = j + 1
            else:
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)
    print("Sau chuan hoa: ")
    print(len(new_en_list))
    print(len(new_vn_list))
    return new_en_list, new_vn_list


def write_process_add(lines_en, lines_vn):
    # print("write_process_add")
    if len(lines_en) != len(lines_vn):
        return
    for i in range(len(lines_en)):
        if i == 1:
            continue
        en_text = lines_en[i]
        vn_text = lines_vn[i]
        english_sentences = tokenize_sentences_with_name_prefix(en_text)
        vietnamese_sentences = nltk.sent_tokenize(vn_text)

        if len(english_sentences) == len(vietnamese_sentences):
            # Tạo DataFrame từ danh sách câu tiếng Anh và tiếng Việt đã tách
            df = pd.DataFrame({'English': english_sentences, 'Vietnamese': vietnamese_sentences}, index=None)
            # Ghi vào file 'dic_eng_vn_data.csv'
            df.to_csv('dic_eng_vn_data.csv', mode='a', header=False, index=False)


def write_process(lines_en, lines_vn):
    # print("write_process")
    if len(lines_en) != len(lines_vn):
        return
    for i in range(len(lines_en)):
        en_text = lines_en[i]
        vn_text = lines_vn[i]
        english_sentences = tokenize_sentences_with_name_prefix(en_text)
        vietnamese_sentences = nltk.sent_tokenize(vn_text)
        if len(english_sentences) == len(vietnamese_sentences):
            # Tạo DataFrame từ danh sách câu tiếng Anh và tiếng Việt đã tách
            df = pd.DataFrame({'English': english_sentences, 'Vietnamese': vietnamese_sentences}, index=None)
            # Ghi vào file 'dic_eng_vn_data.csv'
            df.to_csv('dic_eng_vn_data.csv', mode='a', header=False, index=False)


def write_to_csv():
    # Khai bao
    file_name = 'link_eng_vn_gct.csv'
    index_file_name = 'row_number.txt'

    # Lay gia tri
    links_en, links_vn = get_links_from_csv(file_name)
    index = read_number_from_file(index_file_name)
    a =1
    for i in range(index, index + a):
        write_number_to_file(index_file_name, i+1)
        en_link_index = links_en[i]
        vn_link_index = links_vn[i]
        print("link sử dụng: "+ en_link_index)
        print("link sử dụng: " + vn_link_index)
        if "Can not find English Link" in en_link_index:
            # print("Can not find English Link")
            continue

        write_use_link_to_csv(en_link_index, vn_link_index)
        en_article_content = get_en_article_content(en_link_index)
        vn_article_content = get_vn_article_content(vn_link_index)
        article_title = get_en_article_title(en_link_index)

        text_normalization_en = text_normalization_en_f(en_article_content)
        text_normalization_vn = text_normalization_vn_f(vn_article_content)
        if len(text_normalization_en) != len(text_normalization_vn):
            print(en_link_index)
            print(vn_link_index)
            write_not_use_link_to_csv(en_link_index, vn_link_index)
            text_normalization_en, text_normalization_vn = paragraph_indentation(text_normalization_en,
                                                                                 text_normalization_vn)

        """
        # debug
        write_to_text('en_article.txt', en_article_content)
        write_to_text('vn_article.txt', vn_article_content)
        write_list_to_txt('en_article.txt_normalization.txt', text_normalization_en)
        write_list_to_txt('vn_article.txt_normalization.txt', text_normalization_vn)

        print(en_link_index)
        print(vn_link_index)
        print(len(text_normalization_en))
        print(len(text_normalization_vn))
        print(text_normalization_vn)
        print(text_normalization_en)
        """

        if "Additional Persecution News" in article_title:
            write_process_add(text_normalization_en, text_normalization_vn)
        else:
            write_process(text_normalization_en, text_normalization_vn)
    write_number_to_file(index_file_name, index + a)


write_to_csv()

# Khai báo URL
en_url = 'https://en.minghui.org/html/articles/2023/7/6/210192.html'
vn_url = 'https://vn.minghui.org/news/250634-tin-tuc-bo-sung-ve-cuoc-buc-hai-tai-trung-quoc-ngay-6-thang-6-nam-2023.html'

# Khai báo file name
file_name_en = 'article_en.txt'
file_name_vn = 'article_vn.txt'

# bắt đầu ghi


# Lấy Nội dụng web
# content_en = get_en_article_content(en_url)
# content_vn = get_vn_article_content(vn_url)

# en_paragraphs = content_en.split('\n\n')
# vn_paragraphs = content_vn.split('\n\n')

# print (en_paragraphs)

# write
# write_to_text(file_name_en,content_en)
# write_to_text(file_name_vn, content_vn)


# Ghi ra file text
# write_to_text(file_name_en, content_en)
# write_to_text(file_name_vn, content_vn)
# write_to_csv(content_en, content_vn)


"""
file_path = 'link_eng_vn_gct.csv'
links_en, links_vn = get_links_from_csv(file_path)

# Lấy danh sách link tiếng Anh
print(links_en)

# Lấy danh sách link tiếng Việt
print(links_vn)
"""

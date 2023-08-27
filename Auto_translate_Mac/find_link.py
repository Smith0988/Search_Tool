import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_related_link(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_contents_1 = soup.find('div', class_='article-body-content')
        article_contents_2 = soup.find('div', class_='articleZhengwen geo cBBlack')
        if article_contents_1:
            article_contents = article_contents_1
        else:
            article_contents = article_contents_2
        if article_contents:
            paragraphs = article_contents.find_all(['p', 'h3'])
            valid_paragraphs = []
            start_collecting = False
            related_links = []
            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)

                if "Related article" in text or "Related Article" in text or "Related Report" in text or "Related report" in text:
                    start_collecting = True

                if start_collecting:
                    valid_paragraphs.append(text)
                    for link in paragraph.find_all('a', href=True):
                        related_links.append(link['href'])

            if valid_paragraphs:
                article_content = "\n".join(valid_paragraphs)
                return valid_paragraphs, related_links
            else:
                return [], related_links
        else:
            return [], []
    else:
        return [], []

def find_vietnamese_link(english_link):
    first_text = "Bài liên quan:"
    all_link = []
    result_link = []
    result_link.append(first_text)
    link_fail = "Can not find Vietnamese Link"
    # Đọc dữ liệu từ file CSV
    csv_filename = "link_eng_vn_gct.csv"
    df = pd.read_csv(csv_filename)
    related_content, related_link = get_related_link(english_link)
    for link in related_link:
        all_link.append(link)

    for link in all_link:
        # Tìm link tiếng Anh trong cột 1
        row = df[df.iloc[:, 0] == link]

        if not row.empty:
            vietnamese_link = row.iloc[0, 1]
            result_link.append(vietnamese_link)
        else:
            result_link.append(link_fail)
    return related_content, result_link


def find_vietnamese_link_1(english_link):

    # Đọc dữ liệu từ file CSV
    csv_filename = "link_eng_vn_gct.csv"
    df = pd.read_csv(csv_filename)

    # Tìm link tiếng Anh trong cột 1
    row = df[df.iloc[:, 0] == english_link]

    if not row.empty:
        vietnamese_link = row.iloc[0, 1]
        return vietnamese_link
    else:
        return []

def get_vn_article_title(url):
    try:
        # Tải nội dung của trang web
        response = requests.get(url)

        # Kiểm tra nếu yêu cầu thành công (status code 200)
        if response.status_code == 200:
            # Sử dụng BeautifulSoup để phân tích cú pháp trang web
            soup = BeautifulSoup(response.content, 'html.parser')

            # Tìm thẻ div có class là 'article-title'
            article_title_tag = soup.find('h1', class_='articleTitle cABlue')

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

#url = "https://en.minghui.org/html/articles/2020/6/11/185476.html"

#get_related_link(url)




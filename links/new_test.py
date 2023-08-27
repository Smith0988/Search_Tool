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

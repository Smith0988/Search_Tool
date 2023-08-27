import csv
import pandas as pd
import nltk
import requests
from bs4 import BeautifulSoup
import re


def text_normalization_vn_f(vn_article):
    lines_vn = vn_article.split('\n')
    new_vn_list = []

    for text_vn in lines_vn:

        if "Họ và tên" in text_vn or "Ngày mất" in text_vn or "Giới tính:" in text_vn:
            continue
        if 'Họ và tên' in text_vn or 'Ngày mất' in text_vn or 'Giới tính:' in text_vn:
            continue
        if "Bài liên quan" in text_vn or "Thông tin liên lạc" in text_vn or "Các báo cáo liên quan" in text_vn or "Báo cáo liên quan" in text_vn or "Mọi bài viết, hình ảnh, hay nội dung" in text_vn or "Bài viết chỉ thể hiện quan điểm" in text_vn or "Mọi nội dung đăng trên trang" in text_vn or "danh sách những thủ phạm" in text_vn:
            break

        if 'Bài liên quan''' in text_vn or 'Thông tin liên lạc' in text_vn or 'Các báo cáo liên quan' in text_vn or 'Báo cáo liên quan' in text_vn or 'Mọi bài viết, hình ảnh, hay nội dung' in text_vn or 'Bài viết chỉ thể hiện quan điểm' in text_vn or 'Mọi nội dung đăng trên trang' in text_vn or 'danh sách những thủ phạm' in text_vn:
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


def write_not_use_link_to_csv(text1, text2):
    # Tạo DataFrame với hai cột "English" và "Vietnamese"
    df = pd.DataFrame({'English': [text1], 'Vietnamese': [text2]})

    # Ghi vào file CSV, mode='a' để ghi tiếp dữ liệu nếu file đã tồn tại
    df.to_csv('link_not_use.csv', mode='a', header=False, index=False)


def write_to_text(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)


def write_list_to_txt(filename, lst):
    with open(filename, 'w', encoding='utf-8') as file:
        for item in lst:
            file.write(item + '\n')

def write_not_use_link_to_csv(text1, text2):

    link_vn_new = text2.splitlines()
    link_en_new = text1.splitlines()

    # Tạo DataFrame với hai cột "English" và "Vietnamese"
    df = pd.DataFrame({'English': link_en_new, 'Vietnamese': link_vn_new})

    # Ghi vào file CSV, mode='a' để ghi tiếp dữ liệu nếu file đã tồn tại
    df.to_csv('test.csv', mode='a', header=False, index=False)

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


english_text = """

(Minghui.org) A 59-year-old woman in Zhaoyuan City, Shandong Province, stood trial on June 13, 2023, for her faith in Falun Gong, a mind-body practice that has been persecuted by the Chinese Communist Party since July 1999. The judge didn’t allow Ms. Yang Zuojuan to testify in her own defense and adjourned the session quickly.

Arrest
Ms. Yang and her husband, Mr. Lu Lunwen, were about to go out at around 9 a.m. on May 19, 2022, when they were blocked at their garage by four officers from Zhaoyuan City Domestic Security Office. The police searched their car, garage, and home. They confiscated the couple’s computer, cell phones, and other valuables before taking them away.

The couple were released on bail at around 5 p.m. that day.

Sun Zhaopeng and three other officers from Zhaoyuan City Domestic Security Office deceived the couple into going to their office in March 2023, by claiming that they needed them there to sign some paperwork to end their bail.

The couple went but were not given back the 2,000-yuan bail bond the police had promised to return to them. They signed the paperwork, only to have officer Sun submit their case to the Zhaoyuan City Procuratorate later.

The procuratorate summoned the couple days later, on March 23, but they refused to comply with the demand.

The procuratorate transferred the couple’s case to Kaifa District Police Station on March 28 without giving them any paperwork as required by law. The police station gave the couple another one-year bail and ordered them to report to them once every month.

Prosecutors Liu Yanxia and Jiang Xiuping forwarded Ms. Yang’s case to the Zhaoyuan City Court. She received a notice from the court on May 10 saying that her court date was set for June 13. The notice also included a copy of her indictment.

Mr. Lu’s case status isn’t clear at the time of writing.

Court Hearing
Per the Criminal Procedure Law in China, a court hearing should begin with the presiding judge announcing the opening of the trial, followed by presentation of the court’s investigation of evidence for and against the defendant, the prosecution and the defense attorneys debating the case, and the defendant making a closing statement.

During Ms. Yang’s hearing at Zhaoyuan City Court on June 13, 2023, presiding judge Yang Yunjian only announced the opening of the trial and had the prosecutors read out aloud the prosecution evidence against Ms. Yang (without presenting the actual evidence). There was no presentation of the court’s investigation of evidence. No witnesses were present either.

When Ms. Yang tried to testify in her own defense, the judge said he was unable to remember what she said and ordered her to stop. He then rephrased the few things she had said and asked the clerk to record his words in the court proceedings. As it was not her original defense arguments, Ms. Yang protested against the judge for violating legal procedures.

The judge soon adjourned the session without allowing Ms. Yang to make a closing statement. He ordered to keep Ms. Yang in custody, but the local detention center refused to admit her due to her poor health. She was released on June 20.

Past Persecution
Ms. Yang almost had a mental breakdown after her first marriage failed more than two decades ago. After she took up Falun Gong in 1996, she came to understand that there must be a reason for her divorce. She no longer felt bitter and sad. She became upbeat and later married her current husband, also a Falun Gong practitioner.

After the persecution of Falun Gong began in 1999, Ms. Yang was repeatedly targeted for upholding her faith.

She was arrested on Tiananmen Square in Beijing on February 17, 2000 (the 13th day of the lunar Chinese New Year) and taken back to Zhaoyuan City two days later. She was held in Xinzhuang Police Station, where the police handcuffed her to a pole and tortured her. She and a few other arrested practitioners were also paraded on the street. She wasn’t released until 102 days later.

While she was in detention, Ms. Yang’s mother’s home was raided while their loved ones gathered there for the Chinese New Year celebration.

Ms. Yang went to Beijing to appeal for Falun Gong again in late 2000 and was arrested. She was taken back to Zhaoyuan and held at Bianfang Police Station. She and three other practitioners were kept in a small room there (1 meter wide and 1 meter long) before being taken to Zhaoyuan City Detention Center a few days later. Because Ms. Yang refused to renounce her faith, she was handcuffed and shackled. She was also force-fed. She was released from the detention center 30 days later.

Ms. Yang’s home was raided in February 2001. She was held for a total of 64 days at the Linglong Brainwashing Center and Zhaoyuan City Detention Center.

Ms. Yang worked at a chicken slaughterhouse in 2008. The police raided her dorm and took her to Bianfang Police Station. They tortured her in an attempt to make her rat out other practitioners.

Ms. Yang and her husband were arrested at Jinan Railway Station in November 2014 as they were going on a trip. The police searched them, interrogated them with torture, and raided their home.
"""

vietnamese_text = """
[MINH HUỆ 25-06-2023] Một người phụ nữ 59 tuổi ở thành phố Chiêu Viễn, tỉnh Sơn Đông đã bị xét xử vào ngày 13 tháng 6 năm 2023, vì đức tin của bà vào Pháp Luân Công, một pháp môn tu luyện đã bị Đảng Cộng sản Trung Quốc bức hại từ tháng 7 năm 1999. Thẩm phán không cho bà Dương Tác Quyên tự biện hộ và vội vàng cho kết thúc phiên toà.

Vụ bắt giữ

Vào 9 giờ sáng ngày 19 tháng 5 năm 2022, khi bà Dương và chồng bà là ông Lộ Luận Văn chuẩn bị đi ra ngoài thì 4 cảnh sát của Đội An ninh Nội địa Thành phố Chiêu Viễn chặn họ tại ga-ra. Cảnh sát lục soát xe hơi, ga-ra và căn nhà, tịch thu máy tính, điện thoại di động cùng những tài sản khác của họ, sau đó đưa họ đi. Khoảng 5 giờ chiều hôm đó hai vợ chồng đã được bảo lãnh tại ngoại.

Tháng 3 năm 2023, Tôn Triệu Bằng và 3 cảnh sát của Đội An ninh Nội địa Thành phố Chiêu Viễn đã lừa vợ chồng bà Dương đi tới văn phòng của họ bằng cách nói rằng họ cần hai vợ chồng ký vào một số giấy tờ để làm thủ tục kết thúc bảo lãnh.

Hai vợ chồng đã đi tới đó nhưng không được trả lại khoản phí bảo lãnh 2.000 Nhân dân tệ đã đóng mà cảnh sát từng hứa sẽ trả lại cho họ. Họ đã ký vào giấy tờ và sau đó Tôn đã gửi hồ sơ vụ án đến Viện Kiểm sát Thành phố Chiêu Viễn.

Ngày 23 tháng 3, viện kiểm sát triệu tập họ nhưng họ đã từ chối tới đó.

Ngày 28 tháng 3, viện kiểm sát đã chuyển hồ sơ của họ đến Đồn Công an Quận Khai Phát mà không cung cấp bất kỳ giấy tờ nào cho họ theo yêu cầu của pháp luật. Đồn công an đã ra quyết định để hai vợ chồng thêm 1 năm bảo lãnh và lệnh cho họ phải báo cáo với cảnh sát hàng tháng.

Hai công tố viên Lưu Diễm Hà và Khương Tú Bình đã chuyển hồ sơ của bà Dương đến Toà án Thành phố Chiêu Viễn. Ngày 10 tháng 5, toà án gửi thông báo đến bà Dương rằng bà sẽ phải ra hầu tòa vào ngày 13 tháng 6. Thông báo cũng bao gồm một bản sao bản cáo trạng của bà.

Hiện vẫn chưa rõ tình trạng vụ án của ông Lộ.

Phiên toà xét xử

Theo Luật Tố tụng Hình sự ở Trung Quốc, một phiên toà sẽ bắt đầu khi thẩm phán chủ toạ tuyên bố khai mạc phiên toà, tiếp theo là phần trình bày kết quả điều tra của toà án về chứng cứ ủng hộ cho cáo buộc chống lại bị cáo, công tố viên và luật sư biện hộ tranh luận về vụ án và bị cáo sẽ là người nói lời sau cùng.

Trong phiên toà xét xử bà Dương tại Toà án Thành phố Chiêu Viễn vào ngày 13 tháng 6 năm 2023, thẩm phán chủ toạ Dương Uẩn Kiện chỉ tuyên bố khai mạc phiên toà và để các công tố viên đọc to bằng chứng truy tố chống lại bà Dương (không đưa ra vật chứng), đồng thời cũng không trình bày về quá trình điều tra chứng cứ của toà án. Các nhân chứng cũng không có mặt trước tòa.

Khi bà Dương cố gắng tự biện hộ cho mình thì thẩm phán nói rằng ông ta không thể nhớ được những lời bà nói và lệnh cho bà ngừng lại. Sau đó, ông ta diễn đạt lại vài điều mà bà đã nói, rồi yêu cầu thư ký ghi lại trong quá trình tố tụng của toà án. Vì đó không phải là lập luận bào chữa nguyên gốc của bà Dương, nên bà đã phản đối thẩm phán vì vi phạm trình tự pháp lý.

Thẩm phán sớm kết thúc phiên toà mà không cho bà Dương đưa ra những lời bào chữa cuối cùng của mình. Ông ta lệnh tống giam bà Dương nhưng Trại tạm giam địa phương từ chối nhận bà vì sức khoẻ kém. Bà đã được thả vào ngày 20 tháng 6.

Sự bức hại trong quá khứ

Bà Dương gần như suy sụp tinh thần hoàn toàn sau khi cuộc hôn nhân đầu tiên của bà tan vỡ hơn 20 năm trước. Sau khi tu luyện Pháp Luân Công vào năm 1996, bà đã hiểu ra việc ly hôn của bà hẳn là phải có lý do. Bà không còn thấy đau buồn nữa. Bà trở nên lạc quan và sau đó kết hôn với người chồng hiện tại, cũng là một học viên Pháp Luân Công.

Sau khi cuộc đàn áp Pháp Luân Công bắt đầu vào năm 1999, bà Dương đã liên tục bị nhắm đến vì đức tin của mình.

Ngày 17 tháng 2 năm 2000 (ngày thứ 13 của Tết Nguyên đán), bà bị bắt tại Quảng trường Thiên An Môn và bị đưa trở về thành phố Chiêu Viễn hai ngày sau đó. Bà bị giam ở Đồn Công an Tân Trang. Tại đây, công an còng tay bà vào một cái cột và tra tấn bà. Bà và một vài học viên bị bắt khác cũng bị diễu hành trên đường phố. 102 ngày sau đó bà mới được thả.

Trong khi bà bị giam, nhà của mẹ bà bị lục soát trong lúc người thân của bà đang đoàn viên đón Tết Nguyên đán.

Cuối năm 2000, bà Dương lại đến Bắc Kinh để thỉnh nguyện cho Pháp Luân Công và bị bắt. Bà bị đưa trở về Chiêu Viễn và bị giam ở Đồn Công an Biên Phòng. Bà và 3 học viên khác bị giam trong một căn phòng nhỏ (rộng 1 mét, dài 1 mét) rồi bị đưa đến trại tạm giam Thành phố Chiêu Viễn vài ngày sau đó. Vì bà Dương từ chối từ bỏ đức tin nên bà bị còng tay và xích chân và còn bị bức thực. Bà được thả sau 30 ngày bị nhốt ở đó.

Nhà bà Dương bị lục soát vào tháng 2 năm 2001. Bà bị giam tổng cộng 64 ngày ở Trung tâm Tẩy não Linh Lung và trại tạm giam Thành phố Chiêu Viễn.

Bà Dương làm việc tại một lò mổ gà vào năm 2008. Cảnh sát đã đột nhập vào ký túc xá của bà và đưa bà đến Đồn Công an Biên Phòng. Họ đã tra tấn bà nhằm ép bà tiết lộ về các học viên khác.

Tháng 11 năm 2014, vợ chồng bà Dương bị bắt ở Ga Xe lửa Tế Nam khi họ đang có một chuyến đi. Cảnh sát đã lục soát họ, thẩm vấn họ bằng cách tra tấn và lục soát nhà họ.
"""

# Split the texts into paragraphs
#english_paragraphs = english_text.split("\n")
#vietnamese_paragraphs = vietnamese_text.split("\n")
# Remove empty paragraphs
#english_paragraphs_0 = [p for p in english_paragraphs if p.strip()]
#vietnamese_paragraphs_0 = [p for p in vietnamese_paragraphs if p.strip()]
#english_sentences_1 = tokenize_sentences_with_name_prefix(english_text)
#vietnamese_sentences_1 = tokenize_sentences_with_name_prefix(vietnamese_text)

#write_list_to_txt("English_1.txt", english_paragraphs)
#write_list_to_txt("Vietnamese_1.txt", vietnamese_paragraphs)
#write_list_to_txt("English_2.txt", english_sentences_1)
#write_list_to_txt("Vietnamese_2.txt", vietnamese_sentences_1)


def paragraph_indentation(en_article, vn_article):
    new_en_list = []
    new_vn_list = []
    print(len(en_article))
    print(len(vn_article))
    index = max(len(en_article), len(vn_article)) - min(len(en_article), len(vn_article))
    print(index)
    if len(en_article) > len(vn_article):
        j = 0
        for i in range(len(vn_article)):


            en_text = en_article[i+j]
            vn_text = vn_article[i]

            if j == index:
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)
                continue

            english_sentences = tokenize_sentences_with_name_prefix(en_text)
            vietnamese_sentences = tokenize_sentences_with_name_prefix(vn_text)
            english_sentences_2 = tokenize_sentences_with_name_prefix(en_article[i + j + 1])

            if (len(vietnamese_sentences) != len(english_sentences)) and (
                    len(vietnamese_sentences) == len(english_sentences) + len(english_sentences_2)):

                #print("gia tri J la:  ", j)
                #print("en_text:  ", en_text)
                #print("vn_text:  ", vn_text)
                #print("Độ dài đoạn en thứ", i + j, len(english_sentences))
                #print("Độ dài đoạn vn thứ", i, len(vietnamese_sentences))
                #print("Độ dài đoạn en thứ", i + j+1, len(tokenize_sentences_with_name_prefix(en_article[i + j+1])))

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
            if j == index:
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)
                continue

            english_sentences = tokenize_sentences_with_name_prefix(en_text)
            vietnamese_sentences = tokenize_sentences_with_name_prefix(vn_text)
            vietnamese_sentences_2 = tokenize_sentences_with_name_prefix(vn_article[i + j + 1])
            if (len(vietnamese_sentences) != len(english_sentences)) and (
                    len(english_sentences) == len(vietnamese_sentences) + len(vietnamese_sentences_2)):

                #print("gia tri J la:  ", j)
                #print("en_text:  ", en_text)
                #print("vn_text:  ", vn_text)
                #print("Độ dài đoạn vn thứ", i + j, len(vietnamese_sentences))
                #print("Độ dài đoạn en thứ", i, len(english_sentences))
                #print("Độ dài đoạn vn thứ", i + j+1, len(tokenize_sentences_with_name_prefix(vn_article[i + j+1])))

                temp_list = vn_text + " " + vn_article[i + j + 1]
                new_vn_list.append(temp_list)
                new_en_list.append(en_text)
                j = j + 1
            else:
                new_en_list.append(en_text)
                new_vn_list.append(vn_text)

    print(len(new_en_list))
    print(len(new_vn_list))
    return new_en_list, new_vn_list


#text_normalization_en = text_normalization_en_f(english_text)
#text_normalization_vn = text_normalization_vn_f(vietnamese_text)

#write_list_to_txt("English_1.txt", text_normalization_en)
#write_list_to_txt("Vietnamese_1.txt", text_normalization_vn)
#english_paragraphs_after, vietnamese_paragraphs_after = paragraph_indentation(text_normalization_en, text_normalization_vn)



#write_list_to_txt("English.txt", english_paragraphs_after)
#write_list_to_txt("Vietnamese.txt", vietnamese_paragraphs_after)

#write_not_use_link_to_csv(english_paragraphs_after, vietnamese_paragraphs_after)


url = "https://en.minghui.org/html/articles/2022/12/30/205486.html"
en_article = get_en_article_content(url)
print(en_article)

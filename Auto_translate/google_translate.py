from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def translate_with_google_translate(english_text):
    # Tạo một tùy chọn cho trình duyệt Chrome để chạy ẩn
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Khởi tạo trình duyệt Chrome với tùy chọn ẩn
    driver = webdriver.Chrome(options=chrome_options)

    # Mở trang web Google Translate
    driver.get("https://translate.google.com/?hl=vi&sl=en&tl=vi&op=translate")

    # Chờ cho đến khi ô nhập văn bản hiển thị
    input_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Văn bản nguồn']"))
    )

    # Nhập câu cần dịch
    input_box.send_keys(english_text)

    # Đợi cho đến khi kết quả dịch xuất hiện
    vietnamese_translation_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[@class='ryNqvb']")))

    # Lấy kết quả dịch
    vietnamese_translation = vietnamese_translation_element.text

    # Đóng trình duyệt
    driver.quit()

    return vietnamese_translation

# Câu tiếng Anh cần dịch
english_sentence = "It is unclear if the police have submitted Ms. Liu’s case to the procuratorate at the time of writing"

# Dịch câu tiếng Anh sang tiếng Việt
#vietnamese_translation = translate_with_google_translate(english_sentence)

#print("English:", english_sentence)
#print("Vietnamese:", vietnamese_translation)

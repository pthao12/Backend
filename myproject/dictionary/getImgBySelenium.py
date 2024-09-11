import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def getImgBySelenium(searchTerm):
    #img_start_time = time.time()
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Chạy Chrome không có giao diện người dùng
    chrome_options.add_argument("--no-sandbox")  # Bỏ qua chế độ sandbox để tránh lỗi khi chạy không có giao diện
    chrome_options.add_argument("--disable-dev-shm-usage")  # Bỏ qua lỗi bộ nhớ chia sẻ trong môi trường Docker
    chrome_options.add_argument('--ignore-certificate-errors')  # Bỏ qua lỗi chứng chỉ

    # Cung cấp đường dẫn đến chromedriver.exe
    service = Service(executable_path="C:/Users/vuongbahanh/Documents/Dai_hoc/Ki_he/LearningJapaneseApp/Backend/myproject/dictionary/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(f"https://aisozai.com/irasutoya/search?for={searchTerm}")
        
        # Đợi cho đến khi phần tử img xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='css-k008qs']//img"))
        )
        
        # Tìm phần tử img
        img_element = driver.find_element(By.XPATH, "//div[@class='css-k008qs']//img")
        img_src = img_element.get_attribute('src')
        
        # In ra URL ảnh và trả về
        print(f"Image URL: {img_src}")
        # img_end_time = time.time()
        # print(f"fetch_link took {img_end_time - img_start_time:.4f} seconds")
        return img_src

    except Exception as e:
        # Xử lý lỗi
        print(f"Error: {e}")
        return ""

    finally:
        # Đóng trình duyệt
        #close_end_time = time.time()
        #print(f"fetch_close took {close_end_time - img_start_time:.4f} seconds")
        driver.quit()


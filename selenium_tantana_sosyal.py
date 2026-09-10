import os
import time
from datetime import datetime 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

MAX_DAY = "2026-09-25"
today_str = datetime.now().strftime('%Y-%m-%d')



def post_daily_announcement():
    

    if today_str > MAX_DAY:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Tüm duyurular ({MAX_DAY} tarihine kadar) zaten tamamlandı.")
        return

    # Chrome options setup
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {today_str} gün duyurusu paylaşılıyor...")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options,
    )
    try:
        # Login
        driver.get("https://sosyal.tantanacaz.com/login")
        time.sleep(2)

        username_input = driver.find_element(By.ID, "identifier")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CLASS_NAME, "login-submit")

        username_input.send_keys(os.environ.get('TANTANA_USER'))
        password_input.send_keys(os.environ.get('TANTANA_PASSWORD'))
        login_button.click()

        time.sleep(3) 

        # Announcement posting
        driver.get("https://sosyal.tantanacaz.com/duyurular")
        time.sleep(3)

        new_notice_btn = driver.find_element(By.CLASS_NAME, "announcements-new-button")
        driver.execute_script("arguments[0].click();", new_notice_btn)
        time.sleep(3)

        title_input = driver.find_element(By.ID, "announcement-title")
        content_input = driver.find_element(By.ID, "announcement-body")

        
        title_input.send_keys(f"Daily Announcement {today_str} ")
        content_input.send_keys(f"This is the content of daily announcement {today_str}.")
        
        publish_btn = driver.find_element(By.CLASS_NAME, "announcement-publish-button")
        driver.execute_script("arguments[0].click();", publish_btn)

        time.sleep(3)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {today_str}. gün duyurusu başarıyla gönderildi.")


    except Exception as e:
        print(f"Duyuru eklenirken bir hata oluştu: {e}")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == '__main__':
    post_daily_announcement()
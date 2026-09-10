import os
import time
from datetime import datetime 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

COUNTER_FILE = "counter.txt"
MAX_DAY = 15

# Initialize the current day counter
def get_current_day():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 1
    else:
        return 1

def update_current_day(day):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(day))

def post_daily_announcement():

    # Start chrome headless browser  
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    global current_day

    if current_day > MAX_DAY:
        print("All announcements have been posted.")
        return

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {current_day}. announcement is being posted...")

    # Chrome automation
    driver = webdriver.Chrome(
                                service=Service(ChromeDriverManager().install()), 
                                options=chrome_options,
                            )
    try:
        # Login to the web page
        driver.get("https://sosyal.tantanacaz.com/login")
        time.sleep(2) # wait for the page load

        username_input = driver.find_element(By.ID, "identifier")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CLASS_NAME, "login-submit")

        # Secrets/Environment Variables
        username_input.send_keys(os.environ.get('TANTANA_USER'))
        password_input.send_keys(os.environ.get('TANTANA_PASSWORD'))
        login_button.click()

        time.sleep(3) # wait for login 

        # Announcement posting
        driver.get("https://sosyal.tantanacaz.com/duyurular")
        time.sleep(3)

        new_notice_btn = driver.find_element(By.CLASS_NAME, "announcements-new-button")
        driver.execute_script("arguments[0].click();", new_notice_btn)
        time.sleep(3)

        today_str = datetime.now().strftime('%Y-%m-%d')

        # Fill in the announcement form
        title_input = driver.find_element(By.ID, "announcement-title")
        content_input = driver.find_element(By.ID, "announcement-body")

        title_input.send_keys(f"Daily Announcement {today_str}")
        content_input.send_keys(f"This is the content of daily announcement {today_str}.")
        
        # Click the publish button
        publish_btn = driver.find_element(By.CLASS_NAME, "announcement-publish-button")
        driver.execute_script("arguments[0].click();", publish_btn)

        time.sleep(3)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {current_day}. announcement has been posted successfully.")

        update_current_day(current_day + 1)

    except Exception as e:
        print(f"An error occurred while posting the announcement: {e}")
    finally:
        time.sleep(2)
        driver.quit()

if __name__ == '__main__':

    post_daily_announcement()
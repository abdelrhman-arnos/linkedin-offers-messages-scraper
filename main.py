from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# User settings
LINKEDIN_USERNAME = os.environ.get('LINKEDIN_USERNAME')
LINKEDIN_PASSWORD = os.environ.get('LINKEDIN_PASSWORD')
KEYWORDS = ['offer', 'salary', 'rate', 'contract', 'position', 'remote', 'opportunity', 'full-time', 'part-time']

# Start Selenium browser
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

def linkedin_login():
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    driver.find_element(By.ID, 'username').send_keys(LINKEDIN_USERNAME)
    driver.find_element(By.ID, 'password').send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)

def get_offer_messages():
    driver.get('https://www.linkedin.com/messaging/')
    time.sleep(5)

    offers = []

    # Get conversation threads
    threads = driver.find_elements(By.CSS_SELECTOR, 'li.msg-conversation-listitem')
    for thread in threads:
        thread.click()
        time.sleep(2)

        messages = driver.find_elements(By.CSS_SELECTOR, '.msg-s-message-list__event')
        names = driver.find_elements(By.CSS_SELECTOR, '.msg-s-message-group__name')
        timestamps = driver.find_elements(By.CSS_SELECTOR, '.msg-s-message-group__timestamp')
        for idx, msg in enumerate(messages):
            msg_text = msg.text.lower()
            if any(keyword in msg_text for keyword in KEYWORDS):
                sender = names[idx].text if idx < len(names) else ""
                date = timestamps[idx].text if idx < len(timestamps) else ""
                offers.append({
                    'Sender': sender,
                    'Date': date,
                    'Message': msg.text
                })
        time.sleep(1)
    return offers

if __name__ == "__main__":
    linkedin_login()
    results = get_offer_messages()
    df = pd.DataFrame(results)
    df.to_csv('linkedin_offers.csv', index=False)
    print('Offers saved to linkedin_offers.csv')
    driver.quit()

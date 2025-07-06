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
KEYWORDS = ['offer', 'salary', 'rate', 'b2b' 'contract', 'position', 'remote', 'opportunity', 'full-time', 'part-time']
MAX_THREADS = 30

# UI Selectors
LOGIN_USERNAME_INPUT = (By.ID, 'username')
LOGIN_PASSWORD_INPUT = (By.ID, 'password')
LOGIN_SUBMIT_BUTTON = (By.XPATH, '//button[@type="submit"]')
MESSAGE_THREADS = (By.CSS_SELECTOR, 'li.msg-conversation-listitem')
MESSAGE_CONTENT = (By.CSS_SELECTOR, '.msg-s-message-list__event')
MESSAGE_SENDER_NAME = (By.CSS_SELECTOR, '.msg-s-message-group__name')
MESSAGE_SENDER_LINKEDIN_LINK = (By.CSS_SELECTOR, '.msg-s-message-group__meta a')
MESSAGE_TIMESTAMP = (By.CSS_SELECTOR, '.msg-s-message-group__timestamp')

# Start Selenium browser
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

def linkedin_login():
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    driver.find_element(*LOGIN_USERNAME_INPUT).send_keys(LINKEDIN_USERNAME)
    driver.find_element(*LOGIN_PASSWORD_INPUT).send_keys(LINKEDIN_PASSWORD)
    driver.find_element(*LOGIN_SUBMIT_BUTTON).click()
    time.sleep(5)

def get_offer_messages():
    driver.get('https://www.linkedin.com/messaging/')
    time.sleep(5)

    offers = []

    threads = driver.find_elements(*MESSAGE_THREADS)
    for thread in threads[:MAX_THREADS]:
        thread.click()
        time.sleep(2)

        messages = driver.find_elements(*MESSAGE_CONTENT)
        names = driver.find_elements(*MESSAGE_SENDER_NAME)
        linkedin_links = driver.find_elements(*MESSAGE_SENDER_LINKEDIN_LINK)
        timestamps = driver.find_elements(*MESSAGE_TIMESTAMP)
        skip_thread = False
        for idx, msg in enumerate(messages):
            msg_text = msg.text.lower()
            if 'pick' in msg_text:
                skip_thread = True
                break
            if any(keyword.lower() in msg_text for keyword in KEYWORDS):
                sender = names[idx].text if idx < len(names) else ""
                linkedin_link = linkedin_links[idx].get_attribute('href') if idx < len(linkedin_links) else ""
                date = timestamps[idx].text if idx < len(timestamps) else ""
                offers.append({
                    'Sender': sender,
                    'LinkedIn Link': linkedin_link,
                    'Date': date,
                    'Message': msg.text
                })
        if skip_thread:
            continue
        time.sleep(1)
    return offers

if __name__ == "__main__":
    linkedin_login()
    results = get_offer_messages()
    df = pd.DataFrame(results)
    df.to_csv('linkedin_offers.csv', index=False)
    print('Offers saved to linkedin_offers.csv')
    driver.quit()

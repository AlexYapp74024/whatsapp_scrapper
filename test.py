# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
from bs4.element import Tag, ResultSet
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv

load_dotenv()

# Change to your own chrome data directory
user_data_dir = "C:/Users/alexa/AppData/Local/Google/Chrome/User Data"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

profile = "."
chrome_options.add_argument(f"--profile-directory={profile}")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)

driver.get("https://web.whatsapp.com/")

# Add a delay to allow the site to finish loading
time.sleep(5)  # Adjust the number of seconds as needed

# Loop to check for QR code
qr_code_present = True
while qr_code_present:
    try:
        # Try to find the QR code element
        driver.find_element(
            By.XPATH, "//canvas[@aria-label='Scan this QR code to link a device!']"
        )
        print("Waiting for QR code to be scanned...")
        time.sleep(2)  # Wait a bit before checking again
    except Exception:
        # If the element is not found, assume the QR code has been scanned
        qr_code_present = False
        print("QR code scanned, proceeding...")

        # Add a delay to allow the site to finish loading
        time.sleep(5)  # Adjust the number of seconds as needed

# Find the group chat by its name
group_name = "Oh Yea"
group_chat = driver.find_element(By.XPATH, f"//span[@title='{group_name}']")
group_chat.click()

# Scroll and retrieve messages until we have at least 200
messages: list[Tag] = []
while len(messages) < 5:
    time.sleep(1)

    soup = bs(driver.page_source, "html.parser")

    messages = soup.find_all("div", role="row")

    print(f"Retrieved {len(messages)} messages")

    try:
        application_element = driver.find_element(
            By.XPATH, "//div[@role='application']"
        )
        for _ in range(10):
            application_element.send_keys(Keys.PAGE_UP)
    except Exception as e:
        print("scrolling failed", e)
        pass

# input("Press Enter to continue...")
driver.quit()

# %% Process messages
messageTags: list[ResultSet[Tag]] = [
    m.select("span.selectable-text span") for m in messages
]
texts: list[str] = ["".join([t.text for t in ts]) for ts in messageTags]
texts

# %% Saving messages to file
with open("messages.txt", "w", encoding="utf-8") as file:
    for text in texts:
        file.write(text + "\n")

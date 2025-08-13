#! python3
"""Opens up to 5 web links on a subject/topic using Google search in Chrome."""

import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if len(sys.argv) == 1:
    print("Error: Please provide a search query.")
    sys.exit()

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-link-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.add_argument("--headless")  # Optional: uncomment to run in headless mode

# Setup ChromeDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Bypass webdriver detection
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)


def is_captcha_present():
    "..."
    return driver.find_elements(
        By.CSS_SELECTOR, "#captcha-form"
    ) or driver.find_elements(By.CSS_SELECTOR, "iframe[src*='captcha']")


try:
    print("Googling... (wait a few seconds to appear human)")
    driver.get("https://www.google.com")
    time.sleep(3)

    if is_captcha_present():
        print("\n⚠ CAPTCHA detected! Solve it manually in the browser.")
        try:
            input("Press Enter when done...")
        except EOFError:
            print("No input stream available. Skipping wait...")

    # Search box interaction
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_query = " ".join(sys.argv[1:])
    search_box.send_keys(search_query)
    time.sleep(1.2)
    search_box.send_keys(Keys.RETURN)

    if is_captcha_present():
        print("\n⚠ CAPTCHA detected after search! Solve it manually.")
        try:
            input("Press Enter when done...")
        except EOFError:
            print("No input stream available. Skipping wait...")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
    )

    # Improved result extraction
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.g a")
    urls = []
    for link in search_results:
        href = link.get_attribute("href")
        if href and "google.com" not in href:
            urls.append(href)
        if len(urls) >= 5:
            break

    print(f"Opening {len(urls)} results...")
    for i, url in enumerate(urls, 1):
        driver.execute_script(f"window.open('{url}');")
        print(f"Tab {i}: {url[:60]}...")
        time.sleep(2)

    print("\n✅ Done! Browser will stay open for manual inspection.")
    try:
        input("Press Enter to close when finished...")
    except EOFError:
        print("No input stream detected. Closing automatically.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Possible solutions:")
    print("- Update ChromeDriver to match your Chrome version")
    print("- Try again later (Google might have temporarily blocked you)")
    print("- Use proxies/VPN if this persists")

finally:
    driver.quit()

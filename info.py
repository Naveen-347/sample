from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

def search_company(company_name):
    options = Options()
    options.add_argument("--start-maximized")
    
    # Ensure chromedriver is in PATH or specify executable_path in Service
    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        driver.get("https://mcamasterdata.com")
        wait = WebDriverWait(driver, 15)

        # Wait for the search box
        input_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder*="Enter company"]')))
        
        print(f"Typing company name: {company_name}")
        input_box.clear()

        # Typing character by character (mimicking human typing)
        for char in company_name:
            input_box.send_keys(char)
            time.sleep(0.1)

        # Wait for suggestions to load
        time.sleep(3)

        # Navigate dropdown
        print("Navigating dropdown via keyboard (DOWN + ENTER)...")
        input_box.send_keys(Keys.ARROW_DOWN)
        input_box.send_keys(Keys.ENTER)

        # Wait for company details to appear
        wait.until(EC.presence_of_element_located((By.ID, "companyMasterData")))

        # Extract and print details
        data = driver.find_element(By.ID, "companyMasterData").text
        print("\n--- Company Details ---\n")
        print(data)

    except Exception:
        print("❌ Error occurred:")
        traceback.print_exc()

    finally:
        driver.quit()

if __name__ == "__main__":
    company = input("Enter company name: ")
    search_company(company)

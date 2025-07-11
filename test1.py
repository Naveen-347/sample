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
    
    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        driver.get("https://mcamasterdata.com")
        wait = WebDriverWait(driver, 15)

        # Step 1: Type into the search box
        input_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder*="Enter company"]')))
        input_box.clear()
        for char in company_name:
            input_box.send_keys(char)
            time.sleep(0.1)

        # Step 2: Trigger dropdown (ARROW_DOWN + ENTER)
        time.sleep(1)
        input_box.send_keys(Keys.ARROW_DOWN)
        input_box.send_keys(Keys.ENTER)

        # Step 3: Wait for results to load
        print("Waiting for search results...")
        time.sleep(2)

        links = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "table tbody tr td a")))

        matched = False
        for link in links:
            text = link.text.strip().lower()
            if company_name.lower() in text:
                print(f"Clicking on: {link.text}")
                link.click()
                matched = True
                break

        if not matched:
            print("❌ Company not found in search results.")
            return

        # Step 4: Wait for details to load
        time.sleep(3)
        wait.until(EC.presence_of_element_located((By.ID, "companyMasterData")))

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

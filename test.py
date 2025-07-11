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
        wait = WebDriverWait(driver, 20)

        # Step 1: Type company name
        input_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder*="Enter company"]')))
        input_box.clear()
        for char in company_name:
            input_box.send_keys(char)
            time.sleep(0.1)

        # Step 2: Trigger dropdown
        time.sleep(1)
        input_box.send_keys(Keys.ARROW_DOWN)
        input_box.send_keys(Keys.ENTER)

        # Step 3: Wait for table of results
        print("Waiting for search results...")
        time.sleep(3)

        rows = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "table tbody tr")))

        if not rows:
            print("❌ No results found.")
            return

        # ✅ Click only the first row
        try:
            first_row = rows[0]
            print("🔍 First row HTML:", first_row.get_attribute('innerHTML'))

            link = first_row.find_element(By.TAG_NAME, "a")
            print(f"Clicking on: {link.text.strip()}")
            driver.execute_script("arguments[0].scrollIntoView(true);", link)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", link)  # ✅ JS click
        except Exception as e:
            print("❌ Failed to click first result:", e)
            return

        # Step 4: Wait for company details page
        time.sleep(5)
        try:
            wait.until(EC.presence_of_element_located((By.ID, "companyMasterData")))
        except:
            print("❌ Failed to load company data. URL was:", driver.current_url)
            return

        # Step 5: Extract and print
        data = driver.find_element(By.ID, "companyMasterData").text
        print("\n--- Company Details ---\n")
        print(data)

    except Exception:
        print("❌ General error occurred:")
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    company = input("Enter company name: ")
    search_company(company)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
from collections import defaultdict

# driver.quit()
# Initialize WebDriver
driver = webdriver.Firefox()
driver.get("https://www.amazon.com/ap/signin")

email = input("Enter your email-id: ")
password = input("Enter your password: ")
# Find and fill the email field
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys(email)
email_field.send_keys(Keys.RETURN)

time.sleep(2)  # Wait for next page to load

# Find and fill the password field
password_field = driver.find_element(By.ID, "ap_password")
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

time.sleep(2)
print("Logged in successfully")
driver.close()
options = Options()
options.set_preference("general.useragent.override", 
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

driver = webdriver.Firefox(options=options)
try:
    # Open Amazon Best Sellers page
    driver.get("https://www.amazon.in/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2")

    # Wait until the page loads completely by checking for a specific element
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "zg_left_col1")))

    # Check if search box is present
    try:
        search_box = driver.find_element(By.ID, "twotabsearchtextbox")
        print("Search box found!")
    except Exception as e:
        print("Could not find search box:", str(e))

    # Locate the Best Sellers content
    try:
        elements = driver.find_elements(By.ID, "zg_left_col1")
        # Print each item's text content
        categories = defaultdict(list)  # Dictionary with category names as keys and list of products as values
        current_category = "General"  # Default category
        product_pattern = re.compile(r"#\d+\n(.*?)(\n\d[\d,]*\n₹[\d,.]+)", re.S)  # Match product details

        # Split data based on categories
        for element in elements:
            data = element.text
            lines = data.splitlines()
            for line in lines:
                line = line.strip()
                if "Bestsellers in" in line:  # Identify new category
                    current_category = line.replace("See More", "").strip()
                elif re.match(r"#\d+", line):  # Start capturing product details
                    match = product_pattern.match("\n".join(lines[lines.index(line):]))  # Try to match a product block
                    if match:
                        product_details = match.group(1).strip() + " " + match.group(2).strip()
                        categories[current_category].append(product_details)

            # Output the categorized bestsellers
            for category, products in categories.items():
                print(f"\nCategory: {category}")
                for product in products:
                    print(product)
    except Exception as e:
        print("Error while finding Best Sellers content:", str(e))

finally:
    # Clean up
    print("Terminating browser...")
    time.sleep(3)
    driver.quit()

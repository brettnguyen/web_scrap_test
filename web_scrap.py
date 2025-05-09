import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


# Fix the class selector (multiple classes must be separated by dots)
element_css = ".basic-table__content-1toJPX.cnn-pcl-t6ze6u"

# Define the download folder
download_folder = "downloads"

# Ensure the downloads directory exists
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Set up Selenium WebDriver with Headless Mode using WebDriverManager
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Required for some environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents crashes in Docker/Linux
chrome_options.add_argument("--window-size=1920x1080")  # Optional, set window size
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

prefs = {
    "safebrowsing.enabled": True
}

chrome_options.add_experimental_option("prefs", prefs)

# Use WebDriverManager to handle ChromeDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

try:
    # Open the website
    driver.get("https://www.cnn.com/markets/premarkets")
    time.sleep(30)
    # Wait for the element to be visible (up to 10 seconds)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, element_css))
    )

    # Extract the entire div content (including child elements)
    text = element.get_attribute("innerText")  # Use innerText to get formatted text
    print(f"Extracted Text:\n{text}")

    # Save the extracted text into a CSV file inside "downloads" folder
    csv_file_path = os.path.join(download_folder, "scraped_data.csv")
    df = pd.DataFrame([{"Extracted Text": text}])
    df.to_csv(csv_file_path, index=False)

    print(f"Scraping complete! Data saved to '{csv_file_path}'.")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Close the browser
    driver.quit()
    print("Scraping complete!")

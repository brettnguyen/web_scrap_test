from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set the website URL
url = "https://www.cnn.com/markets/premarkets"

# Fix the class selector (multiple classes must be separated by dots)
element_css = ".basic-table__content-1toJPX.cnn-pcl-t6ze6u"

# Set up Selenium WebDriver with Headless Mode using WebDriverManager
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")  # Required for some environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents crashes in Docker/Linux
chrome_options.add_argument("--disable-gpu")  # Optional, for stability
chrome_options.add_argument("--window-size=1920x1080")  # Optional, set window size

# Use WebDriverManager to handle ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Open the website
    driver.get(url)

    # Wait for the element to be visible (up to 10 seconds)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, element_css))
    )

    # Extract the entire div content (including child elements)
    text = element.get_attribute("innerText")  # Use innerText to get formatted text
    print(f"Extracted Text:\n{text}")

    # Save the extracted text into a CSV file
    df = pd.DataFrame([{"Extracted Text": text}])
    df.to_csv("scraped_data.csv", index=False)
    print("Scraping complete! Data saved to 'scraped_data.csv'.")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Close the browser
    driver.quit()
    print("Scraping complete!")

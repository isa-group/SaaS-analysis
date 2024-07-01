from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import csv

PLACEHOLDER_TEXT = "Enter a URL or words related to a site’s home page"
YEARS_TO_ANALYZE = [
    {
        "year": 2019,
        "month": "NOV",
        "second_try": "OCT"
    },
    {
        "year": 2020,
        "month": "NOV",
        "second_try": "OCT"
    },
    {
        "year": 2021,
        "month": "NOV",
        "second_try": "OCT"
    },
    {
        "year": 2022,
        "month": "NOV",
        "second_try": "OCT"
    },
    {
        "year": 2023,
        "month": "NOV",
        "second_try": "OCT"
    },
    {
        "year": 2024,
        "month": "JUL",
        "second_try": "JUN"
    },
]

SAAS_DATA_PATH = '../data/pricings_dataset.csv'
AVAILABLES_DATA_PATH = '../data/available_snapshots.csv'

class ChromeDriver():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)
    
    def generate_new_driver(self, saas):
        self.driver.close()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(2)

        extract_saas_data(saas)

driver_manager = ChromeDriver()

def extract_saas_data(saas):
    try:
        driver_manager.driver.get("https://web.archive.org")
        formatted_url = saas["url"].split("?")[0]

        url_input_element = driver_manager.driver.find_element(By.XPATH, f"//input[@placeholder='{PLACEHOLDER_TEXT}']")
        url_input_element.send_keys(formatted_url)
        url_input_element.send_keys(Keys.RETURN)

        for year in YEARS_TO_ANALYZE:

            year_element = driver_manager.driver.find_element(By.XPATH, f"//span[text()='{year['year']}']")
            year_element.click()
            month = driver_manager.driver.find_element(By.XPATH, f"//div[div[text()='{year['month']}']]")

            snapshots = month.find_elements(By.XPATH, f"//div[@class='calendar-day ']")
            used_second_try = False

            if len(snapshots) == 0:
                month = driver_manager.driver.find_element(By.XPATH, f"//div[div[text()='{year['second_try']}']]")
                snapshots = month.find_elements(By.XPATH, f"//div[@class='calendar-day ']")
                used_second_try = True

            with open(AVAILABLES_DATA_PATH, 'a') as f:
                f.write(f"{saas['name']},{year['month'] if used_second_try else year['second_try']},{year['year']},{len(snapshots) > 0}\n")
    except:
        available_on_the_web = driver_manager.driver.find_elements(By.XPATH, "//*[text()='Wayback Machine has not archived that URL.']")
        if len(available_on_the_web) > 0:
            with open(AVAILABLES_DATA_PATH, 'a') as f:
                for year_to_write in YEARS_TO_ANALYZE:
                    f.write(f"{saas['name']},{year_to_write['month']},{year_to_write['year']},{False}\n")
        else:
            driver_manager.generate_new_driver(saas)

def remove_duplicates(file_path):
    lines = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if line not in lines:
                lines.append(line)

    with open(file_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

if __name__ == '__main__':

    saas_list = pd.read_csv(SAAS_DATA_PATH).to_dict('records')
    
    with open(AVAILABLES_DATA_PATH, 'w') as f:
        f.write("name,month,year,has_snapshot\n")

    for saas in saas_list:
        extract_saas_data(saas)

    driver_manager.driver.close()

    remove_duplicates(AVAILABLES_DATA_PATH)
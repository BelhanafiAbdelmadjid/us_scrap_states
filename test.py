from time import sleep
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import re

def init_driver():
    chrome_options = ChromeOptions()
   
    ua = UserAgent()
    user_agent = ua.random
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = uc.Chrome(options=chrome_options)
    return driver


driver = init_driver()
driver.get("https://gaclaims.unclaimedproperty.com/en/Property/SearchIndex")

driver.maximize_window()

class element_attribute_value_to_be(object):
    def __init__(self, locator, attribute, value):
        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the element
        if element.get_attribute(self.attribute) == self.value:
            return element
        else:
            return False

locator = (By.ID, "divCheckTheBox")
WebDriverWait(driver, 1000).until(
    element_attribute_value_to_be(locator, "style", "display: none;")
)

input_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "submitStandard"))
)

# Click the input element
input_element.click()


parent_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".PagedList-skipToLast"))
)

# Find the <a> element inside the parent element
a_element = parent_element.find_element(By.TAG_NAME, "a")

# Get the content of the <a> element
a_last_link = a_element.get_attribute("href")
page_numbers = int(re.search(r'page=(\d+)', a_last_link).group(1))
a_last_link = re.sub(r'page=\d+&', '', a_last_link)
big_result = []
for i in range(1,page_numbers+1):
    fetch_link = a_last_link + f'&page={i}'
    driver.get(fetch_link)
    parent_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchTable"))
        )
    table_row = driver.find_element(By.ID, "searchTable")
    if i == 1 :
        table_headers = table_row.find_elements(By.TAG_NAME, "th")
        headers = []
        for header_text in table_headers:
            header_text = header_text.text.strip()  # Get the text and strip any surrounding whitespace
            if len(header_text) == 0 :
                headers.append("N")
            else :
                headers.append(header_text)
    table_row = table_row.find_elements(By.TAG_NAME, "tr")
    rows = []
    for row in table_row:
        class_name = row.get_attribute("class").strip(" ")
        try :
            class_name = int(class_name)
            rows.append(row)
        except :
            pass
    # mini_result = []
    for row in rows :
        tds = row.find_elements(By.TAG_NAME, "td")
        i = 0
        mini_dict = {}
        for td in tds :
            if headers[i]  != "N" :
                mini_dict[headers[i]] = tds[i].get_attribute("innerHTML").strip()
            i = i +1 
        big_result.append(mini_dict)
    # big_result = big_result + mini_result 
f = open(f'TEST.json',"a")
json.dump(big_result, f, ensure_ascii=False, indent=4)
driver.quit()



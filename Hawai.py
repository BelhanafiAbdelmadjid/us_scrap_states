from time import sleep
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC




options = ChromeOptions()
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver = uc.Chrome(options=options)

driver.execute_cdp_cmd("Network.enable", {})

driver.get("https://unclaimedproperty.ehawaii.gov/lilo/property-search.html")

last_name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "businessName"))
            )
last_name_input.send_keys("test") 

print("Please solve the reCaptcha manually. Waiting...")
WebDriverWait(driver, 100).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "alert-info")))
WebDriverWait(driver, 100).until(EC.invisibility_of_element_located((By.CLASS_NAME, "alert-info")))
print("reCaptcha solved. Proceeding with automation...")
    

sleep(1000)


recaptcha_btn = ""
recaptcha_btn.click()
# WebDriverWait(driver, 100).until(EC.invisibility_of_element_located((By.CLASS_NAME, "alert-info")))

search_button = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.mt-3')
search_button.click()

driver.quit()
    
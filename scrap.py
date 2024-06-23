from time import sleep
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re

# from web_app import app
from bs4 import BeautifulSoup

def render_html_or_none(input_string):
    try:
        # Attempt to parse the input string as HTML
        soup = BeautifulSoup(input_string, 'html.parser')
        
        if not soup.find():
            return False , None
        
        # Return the rendered text from the HTML
        str = soup.get_text()
        if len(str) == 0 :
            str = "None"
        return True , str
    except Exception as e:
        # If parsing fails, return "None"
        return "None"

def extract_price(price_str):
    if isinstance(price_str, str):
        match = re.match(r'\$(\d+\.\d{2})', price_str)
        if match:
            return float(match.group(1))
        return None
    return None


from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

def init_driver():
    chrome_options = ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = uc.Chrome(options=chrome_options)
    return driver

def sort_fitler(json_body,number_based,looking_for_amount_str_array):
    # json_body = json.loads(body)
    target_properties = []
    if  number_based is None :
        if len(looking_for_amount_str_array) == 0 : 
            target_properties = json_body["properties"]
        else :
            for property in json_body["properties"] :
                if ('propertyValueDescription' in property and property["propertyValueDescription"].strip() in looking_for_amount_str_array)  :
                    # or ('propertyValue' in property and property["propertyValue"].strip() in looking_for_amount_str_array )
                    target_properties.append(property)
    elif number_based["type"] == "float" :
        target_properties = sorted(json_body["properties"], key=lambda x: float(x[number_based["attribute"]]), reverse=True)
    elif number_based["type"] == "$float":
        cleaned_array = []
        not_cleaned_array = []

        for prop in json_body["properties"]:
            new = prop 
            try :
                new[number_based["attribute"]] = float(new[number_based["attribute"]].strip("$")) 
                cleaned_array.append(new)
            except :
                not_cleaned_array.append(new)
        
        target_properties = sorted(cleaned_array, key=lambda x: float(x[number_based["attribute"]]), reverse=True)
        target_properties = target_properties + not_cleaned_array
    return target_properties


def scrap_properties(commonNames,state,lastNameInputID,ButtonSubmitID,fetch_link,target_url,looking_for_amount_str_array,number_based,method,filter_on_attribute=None,state_conf=None):
    driver = init_driver()
    driver.execute_cdp_cmd("Network.enable", {})

    if method == 1 :
        driver.get(fetch_link)
        resuts = []
        for commonName in commonNames:
            last_name_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, lastNameInputID))
                )
            last_name_input.clear()
            last_name_input.send_keys(commonName)  
                
            recaptcha_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, ButtonSubmitID))
            )
            recaptcha_btn.click()
            WebDriverWait(driver, 100).until(EC.invisibility_of_element_located((By.CLASS_NAME, "alert-info")))

            pull_request_found = False
            while not pull_request_found :
                browser_log = driver.get_log('performance') 
                for log in browser_log:
                    message = json.loads(log['message'])['message']
                    if 'response' in message["params"]:
                        
                        if message['params']["response"]["url"] == target_url :
                            pull_request_found = True
                            
                            i =0
                            while True :
                                i = i + 1
                                try :
                                    body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': message['params']['requestId']})['body']
                                    json_body = json.loads(body)
                                    
                                    # target_properties = []
                                    # if  number_based is None :
                                    #     if len(looking_for_amount_str_array) == 0 : 
                                    #         target_properties = json_body["properties"]
                                    #     else :
                                    #         for property in json_body["properties"] :
                                    #             if ('propertyValueDescription' in property and property["propertyValueDescription"].strip() in looking_for_amount_str_array)  :
                                    #                 # or ('propertyValue' in property and property["propertyValue"].strip() in looking_for_amount_str_array )
                                    #                 target_properties.append(property)
                                    # elif number_based["type"] == "float" :
                                    #     target_properties = sorted(json_body["properties"], key=lambda x: float(x[number_based["attribute"]]), reverse=True)
                                    # elif number_based["type"] == "$float":
                                    #     cleaned_array = []
                                    #     not_cleaned_array = []

                                    #     for prop in json_body["properties"]:
                                    #         new = prop 
                                    #         try :
                                    #             new[number_based["attribute"]] = float(new[number_based["attribute"]].strip("$")) 
                                    #             cleaned_array.append(new)
                                    #         except :
                                    #             not_cleaned_array.append(new)
                                        
                                    #     target_properties = sorted(cleaned_array, key=lambda x: float(x[number_based["attribute"]]), reverse=True)
                                    #     target_properties = target_properties + not_cleaned_array

                                    target_properties = sort_fitler(json_body=json_body,number_based=number_based,looking_for_amount_str_array=looking_for_amount_str_array)


                                    resuts = resuts + target_properties
                                    f = open(f'{state}-{commonName}-{datetime.now().date()}.json',"a")
                                    json.dump(target_properties, f, ensure_ascii=False, indent=4)
                                    break
                                except Exception as e :
                                    sleep(1)
                                    if i > 5 :
                                        # resuts.append(
                                        #     {
                                        #         commonName : None
                                        #     }
                                        # )
                                        break
                                    pass
        driver.quit()
        return resuts
    elif method == 2 :
    
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

        for commonName in commonNames:
            result=[]
            driver.get(fetch_link)
            driver.maximize_window()
            for input in state_conf["more_to_check"] :
                element = driver.find_element(input["BY"], input["VALUE"])
                element.click() 
            last_name_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, lastNameInputID))
                    )
            last_name_input.clear()
            last_name_input.send_keys(commonName)  

            print("wainting")
            locator = (By.ID, "divCheckTheBox")
            WebDriverWait(driver, 1000).until(
                element_attribute_value_to_be(locator, "style", "display: none;")
            )
            print("done")

            input_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((ButtonSubmitID["BY"], ButtonSubmitID["VALUE"]))
            )
            
            input_element.click()
            parent_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((state_conf["pagination"]["BY"], state_conf["pagination"]["VALUE"]))
            )
            parent_element = driver.find_element(state_conf["pagination"]["BY"], state_conf["pagination"]["VALUE"])

            a_element = parent_element.find_element(By.TAG_NAME, "a")

            a_last_link = a_element.get_attribute("href")
            page_numbers = int(re.search(r'page=(\d+)', a_last_link).group(1))
            print("page_numbers",page_numbers)
            a_last_link = re.sub(r'page=\d+&', '', a_last_link)
            big_result = []
            for i in range(1,page_numbers+1):
                fetch_link = a_last_link + f'&page={i}'
                print("fetch_link",fetch_link)
                driver.get(fetch_link)
                parent_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((state_conf["table"].get("BY"), state_conf["table"].get("VALUE")))
                    )
                table_row = driver.find_element(state_conf["table"].get("BY"), state_conf["table"].get("VALUE"))
                if i == 1 :
                    table_headers = table_row.find_elements(state_conf["table"]["ROWS"]["BY"], state_conf["table"]["ROWS"]["VALUE"])
                    print(len(table_headers),"table_headers")
                    headers = []
                    for header_text in table_headers:
                        header_text = header_text.text.strip()  
                        if len(header_text) == 0 :
                            headers.append("N")
                        else :
                            headers.append(header_text)
                table_row = table_row.find_elements(By.TAG_NAME, "tr")
                
                rows = []
                for row in table_row:
                    class_name = row.get_attribute("class").strip(" ")
                    if state_conf["table"].get("ROWS_SPECIAL_CLASSES") :
                        for special_class in state_conf["table"]["ROWS_SPECIAL_CLASSES"] :
                            if special_class in class_name :
                                rows.append(row)
                    elif state_conf["table"].get("ROWS_CLASS_INT") :
                        try :
                            class_name = int(class_name)
                            rows.append(row)
                        except :
                            pass
                
                for row in rows :
                    tds = row.find_elements(By.TAG_NAME, "td")
                    if len(tds) > 1 :
                        i = 0
                        mini_dict = {}
                        for td in tds :
                            if headers[i]  != "N" :
                                str_content = tds[i].get_attribute("innerHTML").strip()
                                check_html = render_html_or_none(tds[i].get_attribute("innerHTML").strip())
                                if check_html[0]:
                                    str_content = check_html[1]
                                mini_dict[headers[i]] = str_content
                            i = i +1 
                        big_result.append(mini_dict)
            
            target_properties = []
            if  number_based is None :
                if len(looking_for_amount_str_array) == 0 : 
                    target_properties = big_result
                else :
                    for property in big_result :
                        if (filter_on_attribute in property and property[filter_on_attribute].strip() in looking_for_amount_str_array)  :
                            target_properties.append(property)
            elif number_based["type"] == "float" :
                target_properties = sorted(big_result, key=lambda x: float(x[number_based["attribute"]]), reverse=True)
            elif number_based["type"] == "$float":
                cleaned_array = []
                not_cleaned_array = []
                for prop in big_result:
                    new = prop 
                    try :
                        new[number_based["attribute"]] = float(new[number_based["attribute"]].strip("$")) 
                        cleaned_array.append(new)
                    except :
                        not_cleaned_array.append(new)
                
                target_properties = sorted(cleaned_array, key=lambda x: float(x[number_based["attribute"]]), reverse=True)
                target_properties = target_properties + not_cleaned_array
                # result = result + target_properties
            result = result + target_properties
        f = open(f'TEST.json',"a")
        json.dump(result, f, ensure_ascii=False, indent=4)
        driver.quit()
        return result
    elif method == 4 :
        #CAPTCHA NO TEXT AND NO PAGINATION
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

        for commonName in commonNames:
            result=[]
            driver.get(fetch_link)
            driver.maximize_window()
            last_name_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, lastNameInputID))
                    )
            last_name_input.clear()
            last_name_input.send_keys(commonName)  
        
            for input in state_conf["more_to_check"] :
                print("by",input["BY"])
                print("value",input["VALUE"])
                element = driver.find_element(input["BY"], input["VALUE"])
                element.click() 

            # captcha_status = driver.find_element(By.ID, 'rc-anchor-container')
            # text = captcha_status.get_attribute("innerHTML").strip()
            # print(text)
            # while text != "Verification expired, check the checkbox again for a new challenge" and text != "Recaptcha requires verification." :
            #     text = captcha_status.get_attribute("innerHTML").strip()

            input_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((ButtonSubmitID["BY"], ButtonSubmitID["VALUE"]))
            )
            print("waiting for captcha")
            input_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((ButtonSubmitID["BY"], ButtonSubmitID["VALUE"]))
            )
            print("got the captcha")

            # Click the input element
            input_element.click()
            
            big_result = []
            parent_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((state_conf["table"].get("BY"), state_conf["table"].get("VALUE")))
                )
            table_row = driver.find_element(state_conf["table"].get("BY"), state_conf["table"].get("VALUE"))
            table_headers = table_row.find_elements(state_conf["table"]["HEADERS"]["BY"], state_conf["table"]["HEADERS"]["VALUE"])
            headers = []
            for header_text in table_headers:
                header_text = header_text.text.strip()  # Get the text and strip any surrounding whitespace
                if len(header_text) == 0 :
                    headers.append("N")
                else :
                    headers.append(header_text)
             
            table_row = table_row.find_elements(state_conf["table"]["ROWS"]["BY"], state_conf["table"]["ROWS"]["VALUE"])
            for row in table_row :
                tds = row.find_elements(By.TAG_NAME, "td")
                i = 0
                mini_dict = {}
                for td in tds :
                    if headers[i]  != "N" :
                        mini_dict[headers[i]] = tds[i].get_attribute("innerHTML").strip()
                    i = i +1 
                big_result.append(mini_dict)
            
            # big_result = sort_fitler(json_body=big_result,number_based=number_based,looking_for_amount_str_array=looking_for_amount_str_array)
            target_properties = []
            if  number_based is None :
                if len(looking_for_amount_str_array) == 0 : 
                    target_properties = big_result
                else :
                    for property in big_result :
                        if (filter_on_attribute in property and property[filter_on_attribute].strip() in looking_for_amount_str_array)  :
                            target_properties.append(property)
            elif number_based["type"] == "float" :
                target_properties = sorted(big_result, key=lambda x: float(x[number_based["attribute"]]), reverse=True)
            elif number_based["type"] == "$float":
                cleaned_array = []
                not_cleaned_array = []
                for prop in big_result:
                    new = prop 
                    try :
                        new[number_based["attribute"]] = float(new[number_based["attribute"]].strip("$")) 
                        cleaned_array.append(new)
                    except :
                        not_cleaned_array.append(new)
                
                target_properties = sorted(cleaned_array, key=lambda x: float(x[number_based["attribute"]]), reverse=True)
                target_properties = target_properties + not_cleaned_array
                result = result + target_properties
            result = result + target_properties
        f = open(f'TEST.json',"a")
        json.dump(result, f, ensure_ascii=False, indent=4)
        driver.quit()
        return result
    elif method == 3 :
        
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

        for commonName in commonNames:
            result=[]
            driver.get(fetch_link)
            driver.maximize_window()
            last_name_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, lastNameInputID))
                    )
            last_name_input.clear()
            last_name_input.send_keys(commonName)  
        
            for input in state_conf["more_to_check"] :
                element = driver.find_element(input["BY"], input["VALUE"])
                element.click() 
            print("waiting for captcha")
            if "captcha" in state_conf and state_conf["captcha"] == True :
                locator = (By.ID, "divCheckTheBox")
                WebDriverWait(driver, 1000).until(
                    element_attribute_value_to_be(locator, "style", "display: none;")
                )
            print("Captcha done")
            input_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((ButtonSubmitID["BY"], ButtonSubmitID["VALUE"]))
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
                    EC.presence_of_element_located((state_conf["table"].get("BY"), state_conf["table"].get("VALUE")))
                    )
                table_row = driver.find_element(state_conf["table"].get("BY"), state_conf["table"].get("VALUE"))
                if i == 1 :
                    table_headers = table_row.find_elements(By.TAG_NAME, "th")
                    print(len(table_headers),"table_headers")
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
                for row in rows :
                    tds = row.find_elements(By.TAG_NAME, "td")
                    i = 0
                    mini_dict = {}
                    for td in tds :
                        if headers[i]  != "N" :
                            mini_dict[headers[i]] = tds[i].get_attribute("innerHTML").strip()
                        i = i +1 
                    big_result.append(mini_dict)
            
            # big_result = sort_fitler(json_body=big_result,number_based=number_based,looking_for_amount_str_array=looking_for_amount_str_array)
            target_properties = []
            if  number_based is None :
                if len(looking_for_amount_str_array) == 0 : 
                    target_properties = big_result
                else :
                    for property in big_result :
                        if (filter_on_attribute in property and property[filter_on_attribute].strip() in looking_for_amount_str_array)  :
                            target_properties.append(property)
            elif number_based["type"] == "float" :
                target_properties = sorted(big_result, key=lambda x: float(x[number_based["attribute"]]), reverse=True)
            elif number_based["type"] == "$float":
                cleaned_array = []
                not_cleaned_array = []
                for prop in big_result:
                    new = prop 
                    try :
                        new[number_based["attribute"]] = float(new[number_based["attribute"]].strip("$")) 
                        cleaned_array.append(new)
                    except :
                        not_cleaned_array.append(new)
                
                target_properties = sorted(cleaned_array, key=lambda x: float(x[number_based["attribute"]]), reverse=True)
                target_properties = target_properties + not_cleaned_array
                result = result + target_properties
            result = result + target_properties
        f = open(f'TEST.json',"a")
        json.dump(result, f, ensure_ascii=False, indent=4)
        driver.quit()
        return result

# scrap_properties(['Tyson',"Smith"],"VIRGINIA",'lastName','btn-recaptcha',"https://www.vamoneysearch.gov/app/claim-search",'https://www.vamoneysearch.gov/SWS/properties',[])
# scrap_properties(['Tyson'],"NORTH-CAROLINA",'lastName','btn-recaptcha','https://unclaimed.nccash.com/app/claim-search','https://unclaimed.nccash.com/SWS/properties',[])
# scrap_properties(['Tyson'],"TEXAS",'lastName','btn-recaptcha','https://www.claimittexas.gov/app/claim-search','https://www.claimittexas.gov/SWS/properties',[])
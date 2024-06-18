from time import sleep
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re

def extract_price(price_str):
    if isinstance(price_str, str):
        match = re.match(r'\$(\d+\.\d{2})', price_str)
        if match:
            return float(match.group(1))
        return None
    return None



def scrap_properties(commonNames,state,lastNameInputID,ButtonSubmitID,fetch_link,target_url,looking_for_amount_str_array,number_based):
    options = ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = uc.Chrome(options=options)

    driver.execute_cdp_cmd("Network.enable", {})

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

# scrap_properties(['Tyson',"Smith"],"VIRGINIA",'lastName','btn-recaptcha',"https://www.vamoneysearch.gov/app/claim-search",'https://www.vamoneysearch.gov/SWS/properties',[])
# scrap_properties(['Tyson'],"NORTH-CAROLINA",'lastName','btn-recaptcha','https://unclaimed.nccash.com/app/claim-search','https://unclaimed.nccash.com/SWS/properties',[])
# scrap_properties(['Tyson'],"TEXAS",'lastName','btn-recaptcha','https://www.claimittexas.gov/app/claim-search','https://www.claimittexas.gov/SWS/properties',[])
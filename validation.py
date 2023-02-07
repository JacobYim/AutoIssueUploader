from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import * 

def login_test(id, pw
# , result, idx
) :
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)    
    enter_to_mcols(driver, id.get(), pw.get())
    time.sleep(1)
    res = None
    try :
        res = driver.find_element(By.XPATH, xpath_create_btn)
    except :
        pass
    
    driver.close()

    if res : 
        # result[idx] = [True]
        return True
        
    else :
        # result[idx] = [False]
        return False
    

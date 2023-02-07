import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from utils import * 

ID = "10896347"
PW = "Teamwork@132411"

driver = webdriver.Chrome('./chromedriver')
enter_to_mcols(driver, ID, PW)
press_create_btn(driver)

res = {
}

project_options = driver.find_element(By.XPATH, '//*[@id="project-options"]')
project_options = list(map(lambda x : x['label'], json.loads(project_options.get_attribute('data-suggestions'))[1]['items']))

res['_list'] = project_options

for po in project_options :
    try : 
        project = driver.find_element(By.XPATH, xpath_project)
        time.sleep(3)
        project.click()
        project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
        project.send_keys(po)
        project.send_keys(Keys.ENTER)
        time.sleep(25)
        project = Select(driver.find_element(By.XPATH, xpath_problem_type))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        options.remove('')
    except :
        options = []
    res[po]={}
    res[po]['_list'] = options
    for o in options :
        try :
            write_problem_type(driver, o)
            project = Select(driver.find_element(By.XPATH, xpath_problem_type_1))
            options1 = list(map(lambda x : x.text, project.options))
            print(options1)
        except :
            options1 = []
        res[po][o]={}
        res[po][o]['_list'] = options1
        for o1 in options1 :
            try :
                write_problem_type_1(driver, o1)
                project = Select(driver.find_element(By.XPATH, xpath_problem_type_2))
                options2 = list(map(lambda x : x.text, project.options))
                print(options2)
            except :
                options2 = []
            res[po][o][o1]={}
            res[po][o][o1]['_list'] = options2




json_object = json.dumps(res, indent=4)
with open("problem_type.json", "w+") as f :
    f.write(json_object)

driver.close()
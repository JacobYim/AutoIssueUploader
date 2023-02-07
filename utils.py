from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time 

xpath_id = '//*[@id="login-form-username"]'
xpath_pw = '//*[@id="login-form-password"]'
xpath_btn = '//*[@id="login"]'

xpath_create_btn = '//*[@id="create_link"]'

xpath_project = '//*[@id="project-field"]'
xpath_summary = '//*[@id="summary"]'
xpath_priority = '//*[@id="priority-field"]'
xpath_from = '//*[@id="customfield_10146"]'

xpath_product_type_1 = '//*[@id="customfield_10211"]'
xpath_product_type_2 = '//*[@id="customfield_10211:1"]'
xpath_test_method_1 = '//*[@id="customfield_10137"]'
xpath_test_method_2 = '//*[@id="customfield_16300"]'

xpath_problem_type = '//*[@id="customfield_10125"]'
xpath_problem_type_1 = '//*[@id="customfield_10210"]'
xpath_problem_type_2 = '//*[@id="customfield_10210:1"]'


xpath_components = '//*[@id="components-textarea"]'
xpath_OEM_platform = '//*[@id="customfield_13100"]'
xpath_env_textbtn = '//*[@id="environment-wiki-edit"]/nav/div/div/ul/li[2]/button'
xpath_desc_textbtn = '//*[@id="description-wiki-edit"]/nav/div/div/ul/li[2]/button'

xpath_affects_version = '//*[@id="versions-textarea"]'
xpath_assignee = '//*[@id="assignee-field"]'
xpath_multi_assignee = '//*[@id="customfield_10101"]'
xpath_vehicle_code = '//*[@id="customfield_10809-textarea"]'

xpath_environment = '//*[@id="mce_11_ifr"]'
xpath_reproductivity = '//*[@id="customfield_10900"]'
xpath_description = '//*[@id="mce_12_ifr"]'

xpath_region = '//*[@id="customfield_11500"]'

xpath_submit_btn = '//*[@id="create-issue-submit"]'

file_uploader_xpath = '//*[@id="attachmentmodule"]/div[2]/div/span/input'

xpath_desc_textbtn = '//*[@id="description-wiki-edit"]/nav/div/div/ul/li[2]/button'
xpath_env_textbtn = '//*[@id="environment-wiki-edit"]/nav/div/div/ul/li[2]/button'


def enter_to_mcols(driver, ID, PW) : 

    driver.get("https://mcols.autoever.com/secure/Dashboard.jspa")
    time.sleep(10)

    id = driver.find_element(By.XPATH, xpath_id)
    id.send_keys(ID)
    pw = driver.find_element(By.XPATH, xpath_pw)
    pw.send_keys(PW)

    btn = driver.find_element(By.XPATH, xpath_btn)
    btn.click()
    time.sleep(10)

def press_create_btn(driver) :
    btn = driver.find_element(By.XPATH, xpath_create_btn)
    btn.click()
    time.sleep(20)

def write_project(driver, content_project) :
    project = driver.find_element(By.XPATH, xpath_project)
    time.sleep(3)
    project.click()
    project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
    project.send_keys(content_project)
    project.send_keys(Keys.ENTER)
    time.sleep(60)

def write_summary(driver, content_summary) :
    project = driver.find_element(By.XPATH, xpath_summary)
    project.clear()
    project.send_keys(content_summary)
    project.send_keys(Keys.ENTER)
    time.sleep(1)

def write_priority(driver, content_priority):
    project = driver.find_element(By.XPATH, xpath_priority)
    project.click()
    project.clear()
    project.send_keys(Keys.BACK_SPACE)
    project.send_keys(content_priority)
    project.send_keys(Keys.ENTER)
    time.sleep(1)

def write_from(driver, content_from):
    project = Select(driver.find_element(By.XPATH, xpath_from))
    project.select_by_visible_text(content_from)
    options = list(map(lambda x : x.text, project.options))
    print(options)
    time.sleep(1)
        
def write_product_type_1(driver, content_product_type_1) :
    project = Select(driver.find_element(By.XPATH, xpath_product_type_1))
    project.select_by_visible_text(content_product_type_1)
    options = list(map(lambda x : x.text, project.options))
    print(options)
    time.sleep(1)

def write_product_type_2(driver, content_product_type_2) :
    project = Select(driver.find_element(By.XPATH, xpath_product_type_2))
    project.select_by_visible_text(content_product_type_2)
    options = list(map(lambda x : x.text, project.options))
    print(options)
    time.sleep(1)

def write_test_method_1(driver, content_test_method_1) :
    project = Select(driver.find_element(By.XPATH, xpath_test_method_1))
    project.select_by_visible_text(content_test_method_1)
    options = list(map(lambda x : x.text, project.options))
    print(options)
    time.sleep(1)

def write_test_method_2(driver, content_test_method_2) :
    project = Select(driver.find_element(By.XPATH, xpath_test_method_2))
    project.select_by_visible_text(content_test_method_2)
    options = list(map(lambda x : x.text, project.options))
    print(options)
    time.sleep(1)

def write_problem_type(driver, content_problem_type) :
    project = Select(driver.find_element(By.XPATH, xpath_problem_type))
    options = list(map(lambda x : x.text, project.options))
    print(options)
    project.select_by_visible_text(content_problem_type)
    time.sleep(1)

def write_problem_type_1(driver, content_problem_type_1) :
    project = Select(driver.find_element(By.XPATH, xpath_problem_type_1))
    options = list(map(lambda x : x.text, project.options))
    print(options)
    project.select_by_visible_text(content_problem_type_1)
    time.sleep(1)

def write_problem_type_2(driver, content_problem_type_2) :
    project = Select(driver.find_element(By.XPATH, xpath_problem_type_2))
    options = list(map(lambda x : x.text, project.options))
    print(options)
    project.select_by_visible_text(content_problem_type_2)
    time.sleep(1)

def write_components(driver, content_components) :
    project = driver.find_element(By.XPATH, xpath_components)
    project.clear()
    project.send_keys(content_components)
    project.send_keys(Keys.ENTER)
    time.sleep(1)

def write_OEM_platform(driver, content_OEM_platform) :
    field = driver.find_element(By.XPATH, xpath_OEM_platform).find_elements(By.TAG_NAME, 'div')
    options = list(map(lambda x : x.text, field))
    checkbox = field[options.index(content_OEM_platform)].find_element(By.TAG_NAME, 'label')
    checkbox.click()
    time.sleep(1)

def write_affects_version(driver, content_affects_version) :
    project = driver.find_element(By.XPATH, xpath_affects_version)
    project.click()
    # project.send_keys(Keys.BACK_SPACE)
    # project.clear()
    project.send_keys(content_affects_version)
    project.send_keys(Keys.ENTER)
    time.sleep(1)

def write_assignee(driver, content_assignee) :
    project = driver.find_element(By.XPATH, xpath_assignee)
    project.click()
    project.send_keys(Keys.BACK_SPACE)
    project.clear()
    project.send_keys(content_assignee)
    time.sleep(3)
    project.send_keys(Keys.ENTER)
# time.sleep(1)
# project.send_keys(Keys.ENTER)
    time.sleep(1)

def write_multi_assignee(driver, content_multi_assignee) :
    project = driver.find_element(By.XPATH, xpath_multi_assignee)
    project.click()
    project.send_keys(Keys.BACK_SPACE)
    project.clear()
    project.send_keys(content_multi_assignee)
    time.sleep(3)
    project.send_keys(Keys.ENTER)
    time.sleep(1)

def write_description(driver, content_description) :

    
    textbtn = driver.find_element(By.XPATH, xpath_desc_textbtn)
    textbtn.click()
    time.sleep(1)
    
    project = project = list(filter(lambda x : x.get_attribute('field-id') == 'description', driver.find_elements(By.CLASS_NAME, "jira-wikifield")))[0]
    project = project.find_element(By.TAG_NAME, 'textarea')
    project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
    time.sleep(1)

    project.send_keys(Keys.BACK_SPACE)
    project.send_keys(content_description)
    time.sleep(1)

def write_environment(driver, content_environment) :

    
    textbtn = driver.find_element(By.XPATH, xpath_env_textbtn)
    textbtn.click()
    time.sleep(1)

    project = list(filter(lambda x : x.get_attribute('field-id') == 'environment', driver.find_elements(By.CLASS_NAME, "jira-wikifield")))[0]
    project = project.find_element(By.TAG_NAME, 'textarea')
    project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
    time.sleep(1)
    
    project.send_keys(Keys.BACK_SPACE)
    project.send_keys(content_environment)
    time.sleep(1)

def write_reproductivity(driver, content_reproductivity) :
    project = Select(driver.find_element(By.XPATH, xpath_reproductivity))
    options = list(map(lambda x : x.text, project.options))
    print(options)
    project.select_by_visible_text(content_reproductivity)
    time.sleep(1)

def write_region(driver, content_region) :
    project = Select(driver.find_element(By.XPATH, xpath_region))
    options = list(map(lambda x : x.text, project.options))
    print(options)
    project.select_by_visible_text(content_region)
    time.sleep(1)

def press_submit(driver):
    project = driver.find_element(By.XPATH, xpath_submit_btn)
    project.click()
    time.sleep(15)

def move_to_issue_page(driver) :
    issue_success_class = 'issue-created-key'
    issue_number = driver.find_element(By.CLASS_NAME, issue_success_class).get_attribute('data-issue-key')
    issue_page = 'https://mcols.autoever.com/browse/{}'.format(issue_number)
    driver.get(issue_page.format(issue_number))
    time.sleep(20)
    return issue_page

def upload_video(driver, video_path):
    id = driver.find_element(By.XPATH, file_uploader_xpath)
    id.send_keys(video_path)

    time.sleep(10)

    timeout = 300
    while True :
        try :
            t = driver.find_element(By.ID, "aui-flag-container")
            if t :
                if timeout == 0 :
                    break
            time.sleep(1)
            timeout-=1
            break
        except :
            pass  
    
    time.sleep(2)

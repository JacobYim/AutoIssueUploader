from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time 
from multiprocessing.pool import ThreadPool
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, InvalidElementStateException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import json
import os
from const import *
import logging


def wait_unitil(by, next_element_xpath_list) :
    def decorator(f) :
        def wrapper(self, *args) :
            # print(arg[0])
            while True :
                try :
                    elems = []
                    by_comp = None
                    if by == 'xpath' :
                        by_comp = By.XPATH
                    elif by == 'class' :
                        by_comp = By.CLASS_NAME

                    for next_element_xpath in next_element_xpath_list :
                        ec_comp = EC.presence_of_element_located((by_comp, next_element_xpath))
                        WebDriverWait(self.driver, 10).until(ec_comp)
                        elem = self.driver.find_element(by_comp, next_element_xpath)
                        if elem :
                            elems.append(elem)
                        else : 
                            elems.append(None)
                    if not None in elems :
                        break
                except (NoSuchElementException, InvalidElementStateException) :
                    pass
            return f(self, *args)
        return wrapper
    return decorator


class Uploader() :

    def __init__(self, driver, ID, PW) :
        self.driver = driver
        self.ID = ID
        self.PW = PW

    def goto(self) :
        self.driver.get("https://mcols.autoever.com/secure/Dashboard.jspa")

        # [xpath_id, xpath_pw, xpath_btn]
    @wait_unitil('xpath',[xpath_id, xpath_pw, xpath_btn])
    def login(self) :
        id = self.driver.find_element(By.XPATH, xpath_id)
        id.send_keys(self.ID)
        pw = self.driver.find_element(By.XPATH, xpath_pw)
        pw.send_keys(self.PW)
        btn = self.driver.find_element(By.XPATH, xpath_btn)
        btn.click()

    @wait_unitil('xpath',[xpath_create_btn])
    def press_create_btn(self) :
        btn = self.driver.find_element(By.XPATH, xpath_create_btn)
        btn.click()

    @wait_unitil('xpath',[xpath_project])
    def write_project(self, content_project) :
        project = self.driver.find_element(By.XPATH, xpath_project)
        project.click()
        project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
        project.send_keys(content_project)
        project.send_keys(Keys.ENTER)
        time.sleep(15)
    
    @wait_unitil('xpath',[xpath_summary])
    def write_summary(self, content_summary) :
        project = self.driver.find_element(By.XPATH, xpath_summary)
        project.clear()
        project.send_keys(content_summary)
        project.send_keys(Keys.ENTER)
    
    @wait_unitil('xpath',[xpath_priority])
    def write_priority(self, content_priority):
        time.sleep(1)
        project = self.driver.find_element(By.XPATH, xpath_priority)
        project.click()
        project.clear()
        project.send_keys(Keys.BACK_SPACE)
        project.send_keys(content_priority)
        project.send_keys(Keys.ENTER)

    @wait_unitil('xpath',[xpath_from])
    def write_from(self, content_from):
        project = Select(self.driver.find_element(By.XPATH, xpath_from))
        project.select_by_visible_text(content_from)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        
    
    @wait_unitil('xpath',[xpath_product_type_1])
    def write_product_type_1(self, content_product_type_1) :
        project = Select(self.driver.find_element(By.XPATH, xpath_product_type_1))
        project.select_by_visible_text(content_product_type_1)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        
    @wait_unitil('xpath',[xpath_product_type_2])
    def write_product_type_2(self, content_product_type_2) :
        project = Select(self.driver.find_element(By.XPATH, xpath_product_type_2))
        project.select_by_visible_text(content_product_type_2)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        
    @wait_unitil('xpath',[xpath_test_method_1])
    def write_test_method_1(self, content_test_method_1) :
        project = Select(self.driver.find_element(By.XPATH, xpath_test_method_1))
        project.select_by_visible_text(content_test_method_1)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        
    @wait_unitil('xpath',[xpath_test_method_2])
    def write_test_method_2(self, content_test_method_2) :
        project = Select(self.driver.find_element(By.XPATH, xpath_test_method_2))
        project.select_by_visible_text(content_test_method_2)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        
    @wait_unitil('xpath',[xpath_problem_type])
    def write_problem_type(self, content_problem_type) :
        project = Select(self.driver.find_element(By.XPATH, xpath_problem_type))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_problem_type)
        

    @wait_unitil('xpath',[xpath_problem_type_1])
    def write_problem_type_1(self, content_problem_type_1) :
        project = Select(self.driver.find_element(By.XPATH, xpath_problem_type_1))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_problem_type_1)
        

    @wait_unitil('xpath',[xpath_problem_type_2])
    def write_problem_type_2(self, content_problem_type_2) :
        project = Select(self.driver.find_element(By.XPATH, xpath_problem_type_2))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_problem_type_2)
        

    @wait_unitil('xpath',[xpath_components])
    def write_components(self, content_components) :
        project = self.driver.find_element(By.XPATH, xpath_components)
        project.clear()
        project.send_keys(content_components)
        project.send_keys(Keys.ENTER)
        

    @wait_unitil('xpath',[xpath_OEM_platform])
    def write_OEM_platform(self, content_OEM_platform) :
        field = self.driver.find_element(By.XPATH, xpath_OEM_platform).find_elements(By.TAG_NAME, 'div')
        options = list(map(lambda x : x.text, field))
        checkbox = field[options.index(content_OEM_platform)].find_element(By.TAG_NAME, 'label')
        checkbox.click()
        

    @wait_unitil('xpath',[xpath_affects_version])
    def write_affects_version(self, content_affects_version) :
        project = self.driver.find_element(By.XPATH, xpath_affects_version)
        project.click()
        # project.send_keys(Keys.BACK_SPACE)
        # project.clear()
        project.send_keys(content_affects_version)
        project.send_keys(Keys.ENTER)
        

    @wait_unitil('xpath',[xpath_assignee])
    def write_assignee(self, content_assignee) :
        project = self.driver.find_element(By.XPATH, xpath_assignee)
        project.click()
        project.send_keys(Keys.BACK_SPACE)
        project.clear()
        project.send_keys(content_assignee)
        time.sleep(3)
        project.send_keys(Keys.ENTER)
    # 
    # project.send_keys(Keys.ENTER)
        

    @wait_unitil('xpath',[xpath_multi_assignee])
    def write_multi_assignee(self, content_multi_assignee) :
        project = self.driver.find_element(By.XPATH, xpath_multi_assignee)
        project.click()
        project.send_keys(Keys.BACK_SPACE)
        project.clear()
        project.send_keys(content_multi_assignee)
        time.sleep(3)
        project.send_keys(Keys.ENTER)
        

    @wait_unitil('xpath',[xpath_desc_textbtn])
    def write_description(self, content_description) :

        textbtn = self.driver.find_element(By.XPATH, xpath_desc_textbtn)
        textbtn.click()
        
        
        project = project = list(filter(lambda x : x.get_attribute('field-id') == 'description', self.driver.find_elements(By.CLASS_NAME, "jira-wikifield")))[0]
        project = project.find_element(By.TAG_NAME, 'textarea')
        project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
        

        project.send_keys(Keys.BACK_SPACE)
        project.send_keys(content_description)
        

    @wait_unitil('xpath',[xpath_env_textbtn])
    def write_environment(self, content_environment) :
        textbtn = self.driver.find_element(By.XPATH, xpath_env_textbtn)
        textbtn.click()
        

        project = list(filter(lambda x : x.get_attribute('field-id') == 'environment', self.driver.find_elements(By.CLASS_NAME, "jira-wikifield")))[0]
        project = project.find_element(By.TAG_NAME, 'textarea')
        project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
        
        
        project.send_keys(Keys.BACK_SPACE)
        project.send_keys(content_environment)
        

    @wait_unitil('xpath',[xpath_reproductivity])
    def write_reproductivity(self, content_reproductivity) :
        project = Select(self.driver.find_element(By.XPATH, xpath_reproductivity))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_reproductivity)
        

    @wait_unitil('xpath',[xpath_region])
    def write_region(self, content_region) :
        project = Select(self.driver.find_element(By.XPATH, xpath_region))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_region)
    
    @wait_unitil('xpath',[xpath_submit_btn])
    def press_submit(self):
        project = self.driver.find_element(By.XPATH, xpath_submit_btn)
        project.click()
        time.sleep(15)

    @wait_unitil('class',[issue_success_class])
    def move_to_issue_page(self) :
        issue_number = self.driver.find_element(By.CLASS_NAME, issue_success_class).get_attribute('data-issue-key')
        issue_page = 'https://mcols.autoever.com/browse/{}'.format(issue_number)
        self.driver.get(issue_page.format(issue_number))
        time.sleep(20)
        return issue_page

    @wait_unitil('xpath',[file_uploader_xpath])
    def upload_video(self, video_path):
        id = self.driver.find_element(By.XPATH, file_uploader_xpath)
        id.send_keys(video_path)
        time.sleep(10)
        timeout = 300
        while True :
            try :
                t = self.driver.find_element(By.ID, "aui-flag-container")
                if t :
                    if timeout == 0 :
                        break
                time.sleep(1)
                timeout-=1
                break
            except :
                pass  
        
        time.sleep(2)

class UploadManager() :

    def __init__(self, id, pw) :
        self.id = id
        self.pw = pw
        logging.info('upload manager Loaded')
    
    def run(self, cur_works, num_pool=3) :
        p = ThreadPool(num_pool)
        res = p.map(self.upload_issue, cur_works)

        with open("{}_output.txt".format(datetime.datetime.now().strftime("%b-%d-%Y-%H-%M-%S")), "w") as f :
            res = json.dumps(res, indent=4)
            f.write(res)
        
    def upload_issue(self, data) :

        ID = self.id
        PW = self.pw

        content_project = data['Project'] 
        content_summary = data['Summary Prefix']+ " " + data['Summary']
        content_priority = data['Priority']
        content_from = data['From']
        content_product_type_1 = data['Product Type']
        content_product_type_2 = data['Product Type Detail']
        content_test_method_1 = data['Test Method 1']
        content_test_method_2 = data['Test Method 2']
        content_problem_type = data['Problem Type']
        content_problem_type_1 = data['Problem Type 1']
        content_problem_type_2 = data['Problem Type 2']
        content_components = data['Components']
        content_OEM_platform = data['OEM Platform']
        content_affects_version = data['Affects Version']
        content_assignee = data['Assignee']
        content_multi_assignee = data['Multi Assignee']
        content_environment = data['Environment']
        content_description = data['Description'].replace('로그:', '로그: {}'.format(data['Log']))
        content_reproductivity = data['Reproductivity']
        content_region = '북미(NAM)'
        data['Video'] = data['Video'] if type(data['Video']) == 'str' else ""
        print(data['Video'])
        video_path = '{}\{}'.format(data['dirpath'], data['Video'].split('\n')[0])
        print(video_path)
        # video_path = 'c:\\Users\\HAEA_MI\\Desktop\\autouploader\\0113\\video\\{}'.format()
    
        retval = {
            "summary" : content_summary,
            "issue" : None,
            "S/F" : False,
            "reason" : None
        }

        try :
            # if not os.path.isfile(video_path) : 
            #     retval["reason"] = "{} is not file".format(video_path)
            #     return retval 
                
            options = Options()
            # options.add_argument('--headless')
            driver = webdriver.Chrome('./chromedriver', chrome_options=options)
            u = Uploader(driver, ID, PW)
            u.goto()
            u.login()
            u.press_create_btn()
            logging.info('START TO WRITE ISSUE FORM   | {}'.format(content_summary))
            u.write_project(content_project)
            u.write_summary(content_summary)
            u.write_priority(content_priority)
            u.write_from(content_from)
            u.write_product_type_1(content_product_type_1) 
            u.write_product_type_2(content_product_type_2) 
            u.write_test_method_1(content_test_method_1)
            try :
                u.write_test_method_2(content_test_method_2) 
            except :
                pass
            u.write_problem_type(content_problem_type) 
            u.write_problem_type_1(content_problem_type_1) 
            u.write_problem_type_2(content_problem_type_2) 
            u.write_components(content_components) 
            u.write_OEM_platform(content_OEM_platform) 
            u.write_affects_version(content_affects_version) 
            u.write_assignee(content_assignee) 
            u.write_multi_assignee(content_multi_assignee) 
            u.write_environment(content_environment) 
            u.write_description(content_description) 
            u.write_reproductivity(content_reproductivity)
            u.write_region(content_region)
            # u.press_submit()
            logging.info('ISSUE FORM WRITTEN SUCCESS  | {}'.format(content_summary))
            issue_page = u.move_to_issue_page()
            logging.info('ISSUE TICKET GENERATED      | {} at {}'.format(content_summary, issue_page))
            retval["issue"]=issue_page
            u.upload_video(video_path)
            logging.info('ISSUE VIDEO UPLOAD SUCCESS  | {}'.format(content_summary))

            driver.close()
            logging.info('ISSUE UPLOAD SUCCESS        | {}'.format(content_summary))
            retval["S/F"]=True

            return retval

        except Exception as e :
            logging.info('ISSUE UPLOAD FAIL           | {}'.format(content_summary))
            logging.info('ERROR                       | {}'.format(e))
            retval["S/F"]=False
            retval["reason"]=str(e)

            return retval
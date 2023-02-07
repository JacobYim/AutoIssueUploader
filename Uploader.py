from msilib.schema import SelfReg
from typing import Self
from const import *
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

def wait_unitil(driver, next_element_xpath_list) :
    def decorator(func) :
        while True :
            try :
                elems = []
                for next_element_xpath in next_element_xpath_list :
                    elem = driver.find_element(By.XPATH, next_element_xpath)
                    elems.append(elem)
                if not None in elems :
                    break
            except NoSuchElementException :
                time.sleep(1)
        res = func()
        time.sleap(1)
        return res
    return decorator


class Uploader() :

    def __init__(self, driver, ID, PW) :
        self.driver = driver
        self.ID = ID
        self.PW = PW

    
    def login(self) :
    
        self.driver.get("https://mcols.autoever.com/secure/Dashboard.jspa")

        
    # @wait_unitil(SelfReg.driver, [xpath_id, xpath_pw, xpath_btn])
    # def login(self) :
    #     id = self.driver.find_element(By.XPATH, xpath_id)
    #     id.send_keys(self.ID)
    #     pw = self.driver.find_element(By.XPATH, xpath_pw)
    #     pw.send_keys(self.PW)
    #     btn = self.driver.find_element(By.XPATH, xpath_btn)
    #     btn.click()

    # @wait_unitil(SelfReg.driver, [xpath_create_btn])
    # def press_create_btn(self) :
    #     btn = self.driver.find_element(By.XPATH, xpath_create_btn)
    #     btn.click()

    # @wait_unitil(SelfReg.driver, [xpath_project])
    # def write_project(driver, content_project) :
    #     project = driver.find_element(By.XPATH, xpath_project)
    #     project.click()
    #     project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
    #     project.send_keys(content_project)
    #     project.send_keys(Keys.ENTER)
    
    # @wait_unitil(SelfReg.driver, [xpath_summary])
    # def write_project(driver, content_summary) :
    #     project = driver.find_element(By.XPATH, xpath_summary)
    #     project.clear()
    #     project.send_keys(content_summary)
    #     project.send_keys(Keys.ENTER)
    

    def goto(self) :
        self.driver.get("https://mcols.autoever.com/secure/Dashboard.jspa")

        # [xpath_id, xpath_pw, xpath_btn]
    @wait_unitil([xpath_id, xpath_pw, xpath_btn])
    def login(self) :
        id = self.driver.find_element(By.XPATH, xpath_id)
        id.send_keys(self.ID)
        pw = self.driver.find_element(By.XPATH, xpath_pw)
        pw.send_keys(self.PW)
        btn = self.driver.find_element(By.XPATH, xpath_btn)
        btn.click()

    @wait_unitil([xpath_create_btn])
    def press_create_btn(self) :
        btn = self.driver.find_element(By.XPATH, xpath_create_btn)
        btn.click()

    @wait_unitil([xpath_project])
    def write_project(self, content_project) :
        project = self.driver.find_element(By.XPATH, xpath_project)
        project.click()
        project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
        project.send_keys(content_project)
        project.send_keys(Keys.ENTER)
        time.sleep(15)
    
    @wait_unitil([xpath_summary])
    def write_summary(self, content_summary) :
        project = self.driver.find_element(By.XPATH, xpath_summary)
        project.clear()
        project.send_keys(content_summary)
        project.send_keys(Keys.ENTER)
    
    @wait_unitil([xpath_priority])
    def write_priority(self, content_priority):
        project = self.driver.find_element(By.XPATH, xpath_priority)
        project.click()
        project.clear()
        project.send_keys(Keys.BACK_SPACE)
        project.send_keys(content_priority)
        project.send_keys(Keys.ENTER)

    @wait_unitil([xpath_from])
    def write_from(self, content_from):
        project = Select(self.driver.find_element(By.XPATH, xpath_from))
        project.select_by_visible_text(content_from)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        
    

    @wait_unitil([xpath_product_type_1])
    def write_product_type_1(self, content_product_type_1) :
        project = Select(self.driver.find_element(By.XPATH, xpath_product_type_1))
        project.select_by_visible_text(content_product_type_1)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        

    @wait_unitil([xpath_product_type_2])
    def write_product_type_2(self, content_product_type_2) :
        project = Select(self.driver.find_element(By.XPATH, xpath_product_type_2))
        project.select_by_visible_text(content_product_type_2)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        

    @wait_unitil([xpath_test_method_1])
    def write_test_method_1(self, content_test_method_1) :
        project = Select(self.driver.find_element(By.XPATH, xpath_test_method_1))
        project.select_by_visible_text(content_test_method_1)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        

    @wait_unitil([xpath_test_method_2])
    def write_test_method_2(self, content_test_method_2) :
        project = Select(self.driver.find_element(By.XPATH, xpath_test_method_2))
        project.select_by_visible_text(content_test_method_2)
        options = list(map(lambda x : x.text, project.options))
        print(options)
        

    @wait_unitil([xpath_problem_type])
    def write_problem_type(self, content_problem_type) :
        project = Select(self.driver.find_element(By.XPATH, xpath_problem_type))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_problem_type)
        

    @wait_unitil([xpath_problem_type_1])
    def write_problem_type_1(self, content_problem_type_1) :
        project = Select(self.driver.find_element(By.XPATH, xpath_problem_type_1))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_problem_type_1)
        

    @wait_unitil([xpath_problem_type_2])
    def write_problem_type_2(self, content_problem_type_2) :
        project = Select(self.driver.find_element(By.XPATH, xpath_problem_type_2))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_problem_type_2)
        

    @wait_unitil([xpath_components])
    def write_components(self, content_components) :
        project = self.driver.find_element(By.XPATH, xpath_components)
        project.clear()
        project.send_keys(content_components)
        project.send_keys(Keys.ENTER)
        

    @wait_unitil([xpath_OEM_platform])
    def write_OEM_platform(self, content_OEM_platform) :
        field = self.driver.find_element(By.XPATH, xpath_OEM_platform).find_elements(By.TAG_NAME, 'div')
        options = list(map(lambda x : x.text, field))
        checkbox = field[options.index(content_OEM_platform)].find_element(By.TAG_NAME, 'label')
        checkbox.click()
        

    @wait_unitil([xpath_affects_version])
    def write_affects_version(self, content_affects_version) :
        project = self.driver.find_element(By.XPATH, xpath_affects_version)
        project.click()
        # project.send_keys(Keys.BACK_SPACE)
        # project.clear()
        project.send_keys(content_affects_version)
        project.send_keys(Keys.ENTER)
        

    @wait_unitil([xpath_assignee])
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
        

    @wait_unitil([xpath_multi_assignee])
    def write_multi_assignee(self, content_multi_assignee) :
        project = self.driver.find_element(By.XPATH, xpath_multi_assignee)
        project.click()
        project.send_keys(Keys.BACK_SPACE)
        project.clear()
        project.send_keys(content_multi_assignee)
        time.sleep(3)
        project.send_keys(Keys.ENTER)
        

    @wait_unitil([xpath_desc_textbtn])
    def write_description(self, content_description) :

        textbtn = self.driver.find_element(By.XPATH, xpath_desc_textbtn)
        textbtn.click()
        
        
        project = project = list(filter(lambda x : x.get_attribute('field-id') == 'description', self.driver.find_elements(By.CLASS_NAME, "jira-wikifield")))[0]
        project = project.find_element(By.TAG_NAME, 'textarea')
        project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
        

        project.send_keys(Keys.BACK_SPACE)
        project.send_keys(content_description)
        

    @wait_unitil([xpath_env_textbtn])
    def write_environment(self, content_environment) :
        textbtn = self.driver.find_element(By.XPATH, xpath_env_textbtn)
        textbtn.click()
        

        project = list(filter(lambda x : x.get_attribute('field-id') == 'environment', self.driver.find_elements(By.CLASS_NAME, "jira-wikifield")))[0]
        project = project.find_element(By.TAG_NAME, 'textarea')
        project.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
        
        
        project.send_keys(Keys.BACK_SPACE)
        project.send_keys(content_environment)
        

    @wait_unitil([xpath_reproductivity])
    def write_reproductivity(self, content_reproductivity) :
        project = Select(self.driver.find_element(By.XPATH, xpath_reproductivity))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_reproductivity)
        

    @wait_unitil([xpath_region])
    def write_region(self, content_region) :
        project = Select(self.driver.find_element(By.XPATH, xpath_region))
        options = list(map(lambda x : x.text, project.options))
        print(options)
        project.select_by_visible_text(content_region)
    
    @wait_unitil([xpath_submit_btn])
    def press_submit(self):
        project = self.driver.find_element(By.XPATH, xpath_submit_btn)
        project.click()
        time.sleep(15)


    def move_to_issue_page(self) :
        issue_success_class = 'issue-created-key'
        issue_number = self.driver.find_element(By.CLASS_NAME, issue_success_class).get_attribute('data-issue-key')
        issue_page = 'https://mcols.autoever.com/browse/{}'.format(issue_number)
        self.driver.get(issue_page.format(issue_number))
        time.sleep(20)
        return issue_page

    @wait_unitil([file_uploader_xpath])
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

    

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import Select
from utils import * 
import pandas as pd
import time



def type_retriever(driver, issue_type = 'Bug') :

    if issue_type == 'Bug' :
        tab = driver.find_element(By.ID, "tab-0")
    else :
        tab = driver.find_element(By.CLASS_NAME, "content")
    children = tab.find_elements(By.XPATH, "*")

    retval = {}

    for idx_child, child in enumerate(children) :

        # initialize inputs
        field_name = None
        input_type = ""
        xpath = None
        required = False

        # check input element is required or not
        if  len(child.find_elements(By.CLASS_NAME, 'icon-required')) > 0 :
            required = True
        else :
            required = False
        
        child_class = child.get_attribute('class')
        if 'field-group' in child_class :
            # find field name
            input_type += 'field-group'
            field_name = child.find_element(By.TAG_NAME, 'label').get_attribute("innerText").split('\n')[0]

            dynamicselects = child.find_elements(By.CLASS_NAME, 'dynamic-select-mark')
            jiramultiselects = child.find_elements(By.CLASS_NAME, 'jira-multi-select')
            cfselects = child.find_elements(By.CLASS_NAME, 'cf-select')
            auissselects  = child.find_elements(By.CLASS_NAME, 'aui-ss-select')
            textareas = child.find_elements(By.CLASS_NAME, 'textarea')
            selects = child.find_elements(By.CLASS_NAME, 'select')
            texts = child.find_elements(By.CLASS_NAME, 'text')
            
            if 'aui-field-cascadingselect' in child_class :
                input_type += " aui-field-cascadingselect"

                retval[field_name] = {
                    'input_type' : input_type+" cascadingselect-parent", 
                    'required' : required,
                    'element' : child.find_element(By.CLASS_NAME, 'cascadingselect-parent')
                }

                field_name+='_sub'
                input_type += " cascadingselect-child" 
                child = child.find_element(By.CLASS_NAME, 'cascadingselect-child')

            elif 'aui-field-labelpicker'in child_class :
                input_type += " aui-field-labelpicker"
            elif 'aui-field-datepicker' in child_class :
                input_type += " aui-field-datepicker"

            elif len(auissselects) == 1 :
                input_type += " aui-ss-select"
            elif len(dynamicselects) == 1 :
                input_type += " dynamic-select-mark"
            elif len(jiramultiselects) == 1 :
                input_type += " jira-multi-select"
            elif len(cfselects) == 1 :
                input_type += " cf-select"
            elif len(textareas) == 1 :
                input_type += " textarea"
            elif len(selects) == 1 :
                input_type += " select"
            elif len(texts) == 1 :
                input_type += " text"

        elif 'fieldset' in child.tag_name :
            # find field name 
            input_type += 'fieldset'
            field_name = child.find_element(By.TAG_NAME, 'legend').get_attribute("innerText").split('\n')[0]
            checkbox_elem = child.find_elements(By.TAG_NAME, 'label')
            file_input_elem = child.find_elements(By.CLASS_NAME, 'file-input-list')
            if len(checkbox_elem) > 0 :
                input_type += ' checkbox' 
            
            elif len(file_input_elem) > 0 :
                input_type += ' file-input-list' 
            
            
        elif 'hidden' in child_class:
            input_type += 'hidden'
        else :
            input_type = None

        retval[field_name] = {
            'input_type' : input_type, 
            'required' : required,
            'element' : child
        }
    return retval

def uploading(data, field_infos) :
    for data_item in data[:1] :
        for key in data_item.to_dict().keys() :
            if not key in ['Project', 'Issue Type'] :
                if key in list(field_infos.keys()):
                    element = field_infos[key]['element']
                    input_content = data_item[key]
                    input_type = field_infos[key]['input_type']
                    if input_content :
                        try :
                            match input_type :
                                case 'field-group dynamic-select-mark' :
                                    element = element.find_element(By.TAG_NAME, 'select')
                                    Select(element).select_by_visible_text(input_content)                        
                                case 'field-group aui-field-cascadingselect cascadingselect-parent' :
                                    Select(element).select_by_visible_text(input_content)
                                case 'field-group aui-field-cascadingselect cascadingselect-child' :
                                    Select(element).select_by_visible_text(input_content)
                                case 'field-group aui-field-datepicker' :
                                    element = element.find_element(By.TAG_NAME, 'input')
                                    element.click()
                                    element.clear()
                                    element.send_keys(Keys.BACK_SPACE)
                                    element.send_keys(input_content)
                                case 'field-group cf-select' :
                                    # print(key)
                                    element = element.find_element(By.TAG_NAME, 'select')
                                    Select(element).select_by_visible_text(input_content)
                                case 'field-group select' :
                                    select_elements = element.find_elements(By.TAG_NAME, 'select')
                                    input_elements = element.find_elements(By.TAG_NAME, 'input')
                                    if len(input_elements) == 1 :
                                        element = input_elements[0]                                
                                        element.click()
                                        element.clear()
                                        element.send_keys(Keys.BACK_SPACE)
                                        element.send_keys(input_content)
                                        element.send_keys(Keys.ENTER)
                                    elif len(select_elements) == 1 :
                                        element = select_elements[0]
                                        Select(element).select_by_visible_text(input_content)
                                case 'field-group jira-multi-select' :
                                    element = element.find_element(By.TAG_NAME, 'textarea')
                                    for item in input_content.split(', ') :
                                        element.send_keys(item)
                                        element.send_keys(Keys.ENTER)
                                case 'field-group text' :
                                    element = element.find_element(By.TAG_NAME, 'input')
                                    if 'ajs-dirty-warning-exempt' in element.get_attribute('class') :
                                        element.click()
                                        element.send_keys(Keys.BACK_SPACE)
                                        element.clear()
                                        element.send_keys(input_content)
                                        time.sleep(3)
                                        element.send_keys(Keys.ENTER)
                                    else :
                                        element.clear()
                                        element.send_keys(input_content)
                                case 'fieldset checkbox' :
                                    field = element.find_elements(By.TAG_NAME, 'div')
                                    options = list(map(lambda x : x.text, field))
                                    checkbox = field[options.index(input_content)].find_element(By.TAG_NAME, 'label')
                                    checkbox.click()
                                case 'field-group textarea' :
                                    if key == 'Description' :
                                        input_content = input_content.replace('[로그:  ]', '[로그: {} ]'.format(data_item['log']))
                                    element = element.find_element(By.CLASS_NAME, 'textarea')
                                    element.click()
                                    element.send_keys(Keys.BACK_SPACE)
                                    element.clear()
                                    element.send_keys(input_content)
                                    time.sleep(3)
                                    element.send_keys(Keys.ENTER)                                                    
                                case 'field-group aui-field-labelpicker' :
                                    element = element.find_element(By.TAG_NAME, 'textarea')
                                    for item in input_content.split(', ') :
                                        element.send_keys(item)
                                        element.send_keys(Keys.ENTER)
                                    pass
                                case 'fieldset file-input-list' :
                                    filepath = 'C:\\Users\\HAEA_MI\\Downloads\\Feb13JXIssueList.txt'
                                    # filepath = 
                                    element = element.find_element(By.CLASS_NAME, 'issue-drop-zone__file')
                                    element.send_keys(filepath)
                                    pass 
                                case 'hidden':
                                    pass
                        except AttributeError as e :
                            print('{} field does not support input {}'.format(key, input_content))
    time.sleep(10)
chromedriver_autoinstaller.install()
options = Options()
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.get("https://mcols.autoever.com/secure/Dashboard.jspa")

ID = "10896665"
PW = "A12345678!"
xlsx_file = 'HMC OEM 내비게이션 개발 협업 (HMCOEM)_03-09-2023-13-29-22.xlsx'

enter_to_mcols(driver, ID, PW)
press_create_btn(driver)

field_infos = type_retriever(driver, issue_type = 'Bug')
df = pd.read_excel(xlsx_file, header=0, index_col=0)
data = list(df[0:100].to_dict('series').values())

uploading(data, field_infos)

# for data_item in data[:1] :
#     for key in data_item.to_dict().keys() :
#         if not key in ['Project', 'Issue Type'] :
#             if key in list(field_infos.keys()):
#                 if field_infos[key]['type'] == 'select' :
#                     field_infos[key]['xpath'].find_element(By.TAG_NAME, 'select')
#                     project = driver.find_element(By.XPATH, xpath_priority)
#                     project.click()
#                     project.clear()
#                     project.send_keys(Keys.BACK_SPACE)
#                     project.send_keys(data_item[key])
#                     project.send_keys(Keys.ENTER)
#                     print(field_infos[key])
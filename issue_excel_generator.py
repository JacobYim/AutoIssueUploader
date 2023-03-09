from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import Select
from utils import * 
import time
import json
from datetime import datetime
import xlsxwriter

def set_project(driver, project_option, issuetype_option) :

    project_field = driver.find_element(By.CLASS_NAME, 'issue-setup-fields').find_element(By.ID, 'project-field')
    project_field.click()
    project_field.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
    project_field.send_keys(project_option)
    project_field.send_keys(Keys.ENTER)

    time.sleep(5)

    issuetype_field = driver.find_element(By.CLASS_NAME, 'issue-setup-fields').find_element(By.ID, 'issuetype-field')
    issuetype_field.click()
    issuetype_field.send_keys(Keys.CONTROL + 'a' + Keys.NULL, '')
    issuetype_field.send_keys(issuetype_option)
    issuetype_field.send_keys(Keys.ENTER)

    time.sleep(5)

def get_project_options(driver) :

    project_fields = driver.find_element(By.CLASS_NAME, 'issue-setup-fields')
    project_options = list(map(lambda x : x['label'], json.loads(project_fields.find_element(By.ID, 'project-options').get_attribute('data-suggestions'))[0]['items']))
    issuetype_options = list(map(lambda x : x['label'], json.loads(project_fields.find_element(By.ID, 'issuetype-options').get_attribute('data-suggestions'))[0]['items']))

    return {
        'projects' : project_options,
        'issuetypes' : issuetype_options
    }

def get_project_input_fields_json(driver, project_name, option, num_recommend_opton = -1) :
    
    tab = driver.find_element(By.ID, "tab-0")
    # field_items = tab.find_elements(By.CLASS_NAME, "field-group") + tab.find_elements(By.TAG_NAME, "fieldset")
    # field_selet_items = list(map(lambda x : {x.text.split('\n')[0]: x.find_elements(By.TAG_NAME, 'select')}, field_items))
    children = tab.find_elements(By.XPATH, "*")

    input_form = {
        "roject" : {
            'type' : 'select',
            'xpath' : None,
            'options' : [project_name],
            'required' : True 
        },
        "issue_type" : {
            'type' : 'select',
            'xpath' : None,
            'options' : [option],
            'required' : True 
        },

    }

    for child in children :

        # initialize inputs
        input_type = None
        xpath = None
        options = None
        required = False

        # check input element is required or not
        if  len(child.find_elements(By.CLASS_NAME, 'icon-required')) > 0 :
            required = True
        else :
            required = False

        child_class = child.get_attribute('class')
        if 'field-group' in child_class :

            i = child

            field_name = child.find_element(By.TAG_NAME, 'label').get_attribute("innerText").split('\n')[0]

            if 'aui-field-datepicker' in child_class :
                input_type = 'date'
                options = ""
                xpath = child

            elif 'frother-control-renderer' in child_class :
                input_type = 'rendering select'
                select_item_list = child.find_elements(By.TAG_NAME, 'select')
                option_list = select_item_list[0].find_elements(By.TAG_NAME, 'option')
                if len(option_list) > num_recommend_opton :
                    option_list = option_list[:num_recommend_opton]
                options = list(map(lambda x : x.get_attribute("innerText").strip(), option_list))
                xpath = child
            
            elif 'aui-field-cascadingselect' in child_class :
                select_item_list = child.find_elements(By.TAG_NAME, 'select')
                if child.get_attribute('style') != "display: none;" :
                    first_select = Select(select_item_list[0])
                    first_options = list(map(lambda x : x.text, first_select.options))
                    second_select = Select(select_item_list[1])
                    options = {}
                    for first_option in first_options :
                        first_select.select_by_visible_text(first_option)
                        second_options = list(map(lambda x : x.text, second_select.options))
                        options[first_option] = second_options
                else :                        
                    last_added_key = list(input_form.keys())[-1]
                    first_select = Select(input_form[last_added_key]['xpath'])
                    first_options = input_form[last_added_key]['options']
                    second_select = Select(select_item_list[0])
                    third_select = Select(select_item_list[1])
                    # options = "tbd"
                    options = {}
                    for first_option in first_options :
                        if first_option :
                            first_select.select_by_visible_text(first_option)
                            second_options = list(map(lambda x : x.text, second_select.options))
                            
                            options[first_option] = {}

                            for second_option in second_options :
                                if second_option :
                                    second_select.select_by_visible_text(second_option)
                                    third_options = list(map(lambda x : x.text, third_select.options))
                                    
                                    options[first_option][second_option] = third_options

                input_type = 'cascading select'
                options = options
                xpath = child
            
            elif 'issue-link-edit' in child_class :
                input_type = 'issue-link-edit'
                select_item_list = child.find_elements(By.TAG_NAME, 'select')
                options = (list(map(lambda x : x.text, Select(select_item_list[0]).options)), list(map(lambda x : x.get_attribute("innerText").strip(), select_item_list[1].find_elements(By.TAG_NAME, 'option'))))
                xpath = child

            elif 'aui-field-labelpicker' in child_class :
                input_type = 'labelpicker'
                options = list(map(lambda x : x.get_attribute("innerText").strip(), child.find_elements(By.TAG_NAME, 'li')))
                xpath = child

            else :
                select_item_list = child.find_elements(By.TAG_NAME, 'select')
                input_list = child.find_elements(By.TAG_NAME, 'input')
                textarea_list = child.find_elements(By.TAG_NAME, 'textarea')

                if len(select_item_list) == 1 :
                    input_type = 'select'
                    options = list(map(lambda x : x.get_attribute("innerText").strip(), select_item_list[0].find_elements(By.TAG_NAME, 'option')))
                    xpath = select_item_list[0]
                elif len(input_list) == 1:
                    input_type = 'input'
                    options = ''
                    xpath = child
                elif len(textarea_list) == 1 :
                    input_type = 'textarea'
                    options = ''' '''
                    xpath = child
                else :
                    input_type = 'Something Went Wrong'
                    options = 'Something Went Wrong'
                    xpath = 'Something Went Wrong'

            print(field_name)


        elif 'fieldset' in child.tag_name :

            # find field name 
            field_name = child.find_element(By.TAG_NAME, 'legend').get_attribute("innerText").split('\n')[0]

            checkbox_elem = child.find_elements(By.TAG_NAME, 'label')
            file_input_elem = child.find_elements(By.CLASS_NAME, 'file-input-list')
            if len(checkbox_elem) > 0 :
                input_type = 'fieldset checkbox' 
                options = list(map(lambda x : x.text, checkbox_elem))
                xpath = child
            
            elif len(file_input_elem) > 0 :
                input_type = 'fieldset file-input-list' 
                options = []
                xpath = child
        
        input_form[field_name] = {
            'type' : input_type,
            'xpath' : xpath,
            'options' : options,
            'required' : required 
        }
        if input_type in ['cascading select', 'issue-link-edit'] :
            input_form[field_name+'_sub'] = {
            'type' : input_type,
            'xpath' : xpath,
            'options' : options,
            'required' : required 
        }

    return input_form

def save_as_xlsx(input_form, filename) :

    workbook = xlsxwriter.Workbook('{}.xlsx'.format(filename))
    # workbook.add_format({'border' : 5})
    worksheet = workbook.add_worksheet()
    worksheet.freeze_panes(1, 1)

    # column numbering
    for i in range(1,100) :
        worksheet.write(0, i, str(i))
        worksheet.set_column("A:ZZ", 30)

    worksheet.write_column('A2', list(input_form.keys())+['log', 'attachments', 'upload status'])

    for i, key in enumerate(input_form.keys()) :

        # required 
        if input_form[key]['required'] :
            worksheet.set_row(i+1, 15, workbook.add_format({'bold': True, 'bg_color': 'yellow'}))

        # set textarea hight
        if input_form[key]['type'] == 'textarea' :
            worksheet.set_row(i+1, 100)

        # set validation
        if input_form[key]['type'] in ['select', 'rendering select', 'fieldset checkbox', 'aui-field-labelpicker'] :
            
            worksheet_name = key.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').lower()
            worksheet_key = workbook.add_worksheet(worksheet_name)
            options = list(map(lambda x : str(x), input_form[key]['options']))
            worksheet_key.write_column('A1', options)
            worksheet.data_validation('B{}:ZZ{}'.format(i+2, i+2), {
                'validate' : 'list',
                'show_error' : False,
                'error_type' : 'information',
                'source': "={}!A1:A{}".format(worksheet_name, len(options))
            })
        elif input_form[key]['type'] in ['cascading select'] :
            
            # parse option table
            option_table = None
            if all(isinstance(n[1], dict) for n in input_form[key]['options'].items()) :
                option_table = list(list(input_form[key]['options'].items())[0][1].items())
            else :
                option_table = list(input_form[key]['options'].items())
            
            if '_sub' in key :
                parent_key = key.split('_sub')[0]
                worksheet_name = parent_key.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').lower()
                
                command_head = ''
                command_end = '"not supported option"'
                for table_row_idx, row in enumerate(option_table) :
                    title, items = row
                    column_alphabet = xlsxwriter.utility.xl_col_to_name(len(items))
                    command_head+= 'IF(B{object_row}="{first_option}", {worksheet}!B{row_number}:{column_alphabet}{row_number}, '.format(first_option=title, worksheet=worksheet_name, object_row=i+1, row_number=1+table_row_idx, column_alphabet=column_alphabet)
                    command_end+=')'

                command = command_head + command_end

            else :
                worksheet_name = key.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').lower()
                worksheet_key = workbook.add_worksheet(worksheet_name)
                options = list(map(lambda x : x[0], option_table))
                
                # fill out the chart
                worksheet_key.write_column('A1', options)
                for idx, elem_tuple in enumerate(option_table) :
                    row_elem_list = elem_tuple[1]
                    worksheet_key.write_row('B{}'.format(idx+1), row_elem_list)    
                    

                command = "={}!A1:A{}".format(worksheet_name, len(options))
            
            # set validation
            worksheet.data_validation('B{}:ZZ{}'.format(i+2, i+2), {
                'validate' : 'list',
                'error_type' : 'information',
                'source': command
            })
    
    workbook.close()

if __name__ == "__main__" :

    ID = "10896665"
    PW = "A12345678!"
    project_name = ""
    issue_type_name = ""
    save_json = True
    show_brower = False

    now = datetime.now() 
    chromedriver_autoinstaller.install()
    options = Options()
    if not show_brower :
        options.headless = True
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.get("https://mcols.autoever.com/secure/Dashboard.jspa")

    enter_to_mcols(driver, ID, PW)
    press_create_btn(driver)
    options = get_project_options(driver)
    if project_name == "" :
        project_name = options['projects'][3]
    if issue_type_name == "" :
        issue_type_name = options['projects'][3]
    set_project(driver, project_name, options['issuetypes'][0])
    json_file = get_project_input_fields_json(driver, project_name, issue_type_name, num_recommend_opton=10)    

    filename = project_name+"_"+now.strftime("%m-%d-%Y-%H-%M-%S")
    if save_json :
        savable_json = json_file.copy()
        for key in savable_json.keys() :
            savable_json[key].pop('xpath')
        with open("{}.json".format(filename), "w", encoding='utf-8') as outfile:
            json.dump(savable_json, outfile, indent="\t", ensure_ascii=False)

    save_as_xlsx(json_file, filename)
    
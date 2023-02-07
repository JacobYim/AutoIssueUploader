from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time 
from utils import * 
from multiprocessing import Pool
import datetime
import json
import os
ID = "10896665"
PW = "A12345678!"

def upload_issue(data) :
    # time.sleep(10)
    print(data)
    # return 0

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
    video_path = 'c:\\Users\\HAEA_MI\\Desktop\\autouploader\\0113\\video\\{}'.format(data['Video'].split('\n')[0])
 
    retval = {
        "summary" : content_summary,
        "issue" : None,
        "S/F" : False,
        "reason" : None
    }

    try :
        if not os.path.isfile(video_path) : 
            retval["reason"] = "{} is not file".format(video_path)
            return retval 
            
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome('./chromedriver', chrome_options=options)

        # exit()
        enter_to_mcols(driver, ID, PW)
        press_create_btn(driver)
        write_project(driver, content_project)
        write_summary(driver, content_summary) 
        write_priority(driver, content_priority)
        write_from(driver, content_from)
        write_product_type_1(driver, content_product_type_1) 
        write_product_type_2(driver, content_product_type_2) 
        write_test_method_1(driver, content_test_method_1) 
        write_test_method_2(driver, content_test_method_2) 
        write_problem_type(driver, content_problem_type) 
        write_problem_type_1(driver, content_problem_type_1) 
        write_problem_type_2(driver, content_problem_type_2) 
        write_components(driver, content_components) 
        write_OEM_platform(driver, content_OEM_platform) 
        write_affects_version(driver, content_affects_version) 
        write_assignee(driver, content_assignee) 
        write_multi_assignee(driver, content_multi_assignee) 
        write_environment(driver, content_environment) 
        write_description(driver, content_description) 
        write_reproductivity(driver, content_reproductivity)
        write_region(driver, content_region)
        press_submit(driver)

        issue_page = move_to_issue_page(driver)
        retval["issue"]=issue_page
        upload_video(driver, video_path)

        time.sleep(10)

        driver.close()
        
        retval["S/F"]=True

        return retval

    except Exception as e :
        retval["S/F"]=False
        retval["reason"]=str(e)

        return retval


if "__main__" == __name__ :

    df = pd.read_excel('issues.xlsx', header=0, index_col=0)
    data = list(df[0:100].to_dict('series').values())
    data = list(filter(lambda x : x['Uploaded'] == 0, data))[:3]
    
    with Pool(3) as p:
        res = p.map(upload_issue, data)

    with open("{}_output.txt".format(datetime.datetime.now().strftime("%b-%d-%Y-%H-%M-%S")), "w") as f :
        res = json.dumps(res, indent=4)
        f.write(res)
    

    # upload_issue(data)

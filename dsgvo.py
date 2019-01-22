from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import re
import datetime


login = "https://www.govos-test.de/govos-test/portal/desktop/0/login" # Login
url_vv_ueberblick="https://www.govos-test.de/govos-test/portal/zs/875/vverfassung?vvid=164_0_0&vvesf=overview" # Uebersicht Verarbeitungsverzeichnis im Verfahren
url_seiten_ueberblick="https://www.govos-test.de/govos-test/portal/zs/875/vverfassung?vvid=164_5_1" # Seitenueberblick xformular
#  "https://www.govos-test.de/govos-test/portal/zs/875/vverfassung/164_5_1?p=1"    seite
url_seite_base="https://www.govos-test.de/govos-test/portal/zs/875/vverfassung/164_"
delay=0.2
version_nr=""
data_nr=""
user="jp@fjd.de"
pages=0
first_page=""

def Klick(_xpath,show_info):
    try:
        elem = driver.find_element_by_xpath(_xpath)
        elem.click()
        time.sleep(delay)
        if(show_info):
            print(driver.current_url, driver.title)
    except:
        pass

def send_user(_xpath,show_info,text):
    elem = driver.find_element_by_xpath(_xpath)
    elem.send_keys(text)
    elem.send_keys(Keys.TAB)
    time.sleep(delay)
    if(show_info):
        print(driver.current_url, driver.title)

def find_version():
    global version_nr
    global data_nr
    driver.get(url_vv_ueberblick)
    vv = "//td[contains(text(),'aktiv')]/../td[1]"
    dv = "//td[contains(text(),'aktiv')]/../td[2]"

    elem_vv = driver.find_element_by_xpath(vv)
    version_nr = elem_vv.get_attribute('innerHTML')
    print("vorlagen-version : "+version_nr)

    elem_dv = driver.find_element_by_xpath(dv)
    data_nr = elem_dv.get_attribute('innerHTML')
    print("daten-version : "+data_nr)

def count_pages():
    global pages
    global first_page
    table_body = driver.find_element_by_xpath("//table[@class='realtable jp-realtable']//tbody")
    rows = table_body.find_elements_by_tag_name("tr")
    anker = rows[0].find_element_by_tag_name("a")
    link = anker.get_attribute('href')
    reg = re.search('\?p=\d+', link)
    rechts = (reg.group(0))
    reg1=re.search('\d+', rechts)
    first_page = (reg1.group(0))
    pages = len(rows)

def fillpage():
    all_div_inputs =  driver.find_elements_by_class_name("xf2-field-input")
    for div in all_div_inputs:
        textarea = 0
        all_inputs = 0

        try:
            all_inputs = div.find_elements_by_tag_name('input')
        except:
            pass

        try:
            textarea = div.find_element_by_tag_name('textarea')
        except:
            pass


        if(len(all_inputs) != 0):  # <input> vorhanden

            if(len(all_inputs)>1):     #  mehr als 1 <input>  radio
                for input in all_inputs:
                    input.click()
            elif(all_inputs[0].get_attribute('type') == 'text'):  # 1 <input>    text
                all_inputs[0].clear()
                all_inputs[0].send_keys("eeeeeeeeeeeeeee")
            elif(all_inputs[0].get_attribute('type') == 'date'):   #  1 <input>  date
                all_inputs[0].clear()
                driver.execute_script('arguments[0].value="2017-06-01"',all_inputs[0])
            elif (all_inputs[0].get_attribute('type') == 'checkbox'):  # 1 <input>  checkbox
                all_inputs[0].click()
            else:
                pass

        if(textarea):
            textarea.clear()
            textarea.send_keys("aaaaaaaaaaaaaaaaaaaaaaa")





driver = webdriver.Firefox()
driver.get(login)
send_user("//input[@name='username']",True,user)
time.sleep(10)
driver.execute_script("window.open('');")# Open a new window This does not change focus to the new window for the driver.
driver.switch_to.window(driver.window_handles[1])# Switch to the new window
find_version() # find active version and data number
driver.get(url_seiten_ueberblick)
count_pages()
driver.get(url_seite_base+version_nr+"_"+data_nr+"?p="+first_page)
while(pages):
    fillpage()
    Klick("//input[@value='weiter >']", True)  # weiter button
    pages-=1

# close the active tab
# driver.close()
# Switch back to the first tab
# driver.switch_to.window(driver.window_handles[0])
# Close the only tab, will also close the browser.
# driver.close()
# driver.get("https://www.govos-test.de/govos-test/portal/zs/875/vverfassung/164_1_5?p=3")
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button







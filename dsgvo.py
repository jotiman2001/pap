from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

login = "https://www.govos-test.de/govos-test/portal/desktop/0/login" # Login
url_vv_ueberblick="https://www.govos-test.de/govos-test/portal/zs/875/vverfassung?vvid=164_0_0&vvesf=overview" # Uebersicht Verarbeitungsverzeichnis im Verfahren
url_seiten_ueberblick="https://www.govos-test.de/govos-test/portal/zs/875/vverfassung?vvid=164_5_1" # Seitenueberblick xformular
#  "https://www.govos-test.de/govos-test/portal/zs/875/vverfassung/164_5_1?p=1"    seite
url_seite_base="https://www.govos-test.de/govos-test/portal/zs/875/vverfassung/164_5_1?p="
delay=0.2
version_nr=""
data_nr=""
user="jp@fjd.de"
pages=0

def Klick(_xpath,show_info):
    elem = driver.find_element_by_xpath(_xpath)
    elem.click()
    time.sleep(delay)
    if(show_info):
        print(driver.current_url, driver.title)

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
    print(version_nr)

    elem_dv = driver.find_element_by_xpath(dv)
    data_nr = elem_dv.get_attribute('innerHTML')
    print(data_nr)

def count_pages():
    global pages
    table_body = driver.find_element_by_xpath("//table[@class='realtable jp-realtable']//tbody")
    rows = table_body.find_elements_by_tag_name("tr")
    pages = len(rows)
    print(len(rows))

driver = webdriver.Firefox()
driver.get(login)
send_user("//input[@name='username']",True,user)
time.sleep(10)
driver.execute_script("window.open('');")# Open a new window This does not change focus to the new window for the driver.
driver.switch_to.window(driver.window_handles[1])# Switch to the new window
find_version() # find active version and data number
driver.get(url_seiten_ueberblick)
while(pages):
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
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button






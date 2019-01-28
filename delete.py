from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import re
login = "https://www.govos-test.de/govos-test/portal/desktop/0/login" # Login
edit = "https://www.govos-test.de/govos-test/portal/desktop/0/index/edit"
delete = "https://www.govos-test.de/govos-test/portal/desktop/0/edit/delete?id="

start = 3188
end = 3195

delay=0.5
user=""
link_list=[]
exception_list = []
ZS=[2460,1825,1678,1415,1407,1393,1007,875,849]
Sonst = [2730,2726,2703,2702,2699,2695,2694,2693]
System = [848]
Edit = [1751,1365,850,613,9]

exception_list.extend(ZS)
exception_list.extend(Sonst)
exception_list.extend(System)
exception_list.extend(Edit)

def Klick(_xpath):
    try:
        elem = driver.find_element_by_xpath(_xpath)
        elem.click()
        time.sleep(delay)
    except:
        pass


def send_user(_xpath,show_info,text):
    elem = driver.find_element_by_xpath(_xpath)
    elem.send_keys(text)
    elem.send_keys(Keys.TAB)
    time.sleep(delay)
    if(show_info):
        print(driver.current_url, driver.title)


driver = webdriver.Firefox()
driver.get(login)
send_user("//input[@name='username']",True,user)
time.sleep(10)
driver.execute_script("window.open('');")# Open a new window This does not change focus to the new window for the driver.
driver.switch_to.window(driver.window_handles[1])# Switch to the new window
driver.get(edit)

links = driver.find_elements_by_xpath("//a[@href]")
for link in links:
    found = re.search("delete",link.get_attribute('href')) # alle links mit delete in link_list
    if(found != None):
        # print(link.get_attribute('href'))
        link_list.append(link.get_attribute('href'))

for link in link_list:
    print(link)

print(exception_list)

i=start

while(i<=end):
        if i in exception_list :
            pass
        else:
            print(i)
            url_del = delete + str(i)
            driver.get(url_del)
            time.sleep(delay)
            # Klick("//input[@value='Bestätigen']")

        i+=1
from selenium import webdriver
import time
login = "https://www.govos-test.de/govos-test/portal/desktop/0/login"
url1="https://www.govos-test.de/govos-test/portal/zs/875/vverfassung"
url2="https://www.govos-test.de/govos-test/portal/zs/875/vverfassung?vvid=164_1_5&vvesf=overview"
url3="https://www.govos-test.de/govos-test/portal/zs/875/vverfassung?vvid=164_1_5"
delay=1
def Klick(_xpath,show_info):
    elem = driver.find_element_by_xpath(_xpath)
    elem.click()
    time.sleep(delay)
    if(show_info):
        print(driver.current_url, driver.title)


driver = webdriver.Firefox()
driver.get(login)
time.sleep(15)
# Open a new window
# This does not change focus to the new window for the driver.
driver.execute_script("window.open('');")


# Switch to the new window
driver.switch_to.window(driver.window_handles[1])
driver.get(url3)
# close the active tab
# driver.close()
# Switch back to the first tab
# driver.switch_to.window(driver.window_handles[0])
# Close the only tab, will also close the browser.
# driver.close()
driver.get("https://www.govos-test.de/govos-test/portal/zs/875/vverfassung/164_1_5?p=3")
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
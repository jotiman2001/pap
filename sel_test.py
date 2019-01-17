

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def Klick(_xpath,show_info):
    elem = driver.find_element_by_xpath(_xpath)
    elem.click()
    time.sleep(delay)
    if(show_info):
        print(driver.current_url, driver.title)

delay=0.2
url="https://www.govos-test.de/govos-test/go/a/288"

driver = webdriver.Firefox()
driver.get(url)
assert "Optionale Registrierung"   in driver.page_source

Klick("//input[@id='h2id0']",False) # no register


Klick("//input[@value='Weiter >']",True) # weiter button


Klick("//a[@class='icon jp-button']",True) # assi starten


Klick('//*[@id="h2id0"]',False) # radio antragtyp


Klick("//*[@id='h2id6']",False) # radio natürl pers


Klick("//input[@value='weiter >']",True) # weiter button

Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='weiter >']",True) # weiter button
Klick("//input[@value='< zurück']",True) # zurück button
Klick("//input[@value='weiter >']",True) # weiter button

Klick("//input[@value='< zurück']",True) # zurück button




time.sleep(2)
driver.close()
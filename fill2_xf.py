from selenium import webdriver
import time
from datetime import date,timedelta
from selenium.webdriver.common.keys import Keys
import re
import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename
from random import *



login = "https://www.govos-test.de/govos-test/portal/desktop/0/login" # Login
url_overview="https://www.govos-test.de/govos-test/portal/antrag2/2974/index/xf2-overview/AGV-0001-GAUTING"
url_base="https://www.govos-test.de/govos-test/portal/antrag2/2974/index/xf2/AGV-0001-GAUTING"

url1="https://www.govos-test.de/govos-test/go/a/301"   #AGV-0001-GAUTING  hundesteuer
# url1="https://www.govos-test.de/govos-test/go/a/288"    # spiel gauting GEWO-021-BY-FL
# url1="https://www.govos-test.de/govos-test/go/a/163"      # BMG 008  Auskunftssperre in das Melderegister gem‰ﬂ ß 51
# url1="https://www.govos-test.de/govos-test/go/a/139"     # UVG_001_TH_FL.xf2
# url1="https://www.govos-test.de/govos-test/go/a/164"      # bedarf
# url1="https://www.govos-test.de/govos-test/go/a/304"      # tl63mo.xf2
# url1 = "https://www.govos-test.de/govos-test/go/a/311"    #  wssxti   Antrag auf Belegungszeiten - Gauting
# url1 = "https://www.govos-test.de/govos-test/go/a/233"    # gewo 26
# url1 = "https://www.govos-test.de/govos-test/go/a/328"     # q7ebyz.xf2
# url1="https://www.govos-test.de/govos-test/go/a/333"        #   udmalf.xf2

delay=0.1
user=""
pages=0
first_page=""
td = timedelta(1)

def check_error():
    try:
        error = driver.find_element_by_class_name("xf2-page-error")  # page error tritt auf
        span = error.find_element_by_tag_name("span")
        message = span.get_attribute("innerHTML")
        return message
    except:                                                         # page error tritt nicht auf
        try:
            error = driver.find_element_by_class_name("xf2-rows-error")  #  rows error tritt auf
            message = error.get_attribute("innerHTML")
            return message
        except:
            return False                                      # rows error tritt nicht auf



def check_eve():
    try:
        eve = driver.find_element_by_name("agreedchecked")
        if (eve):                                   # Einverst‰ndniserkl‰rung
            eve.click()
            Klick("//input[@value='akzeptieren']",True)
    except:
        pass



def log(element):
    name = element.get_attribute("name")
    name = name.lstrip("f")
    attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',element)

    (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = find_type(name)  # get type , subtype ,maxlength,select from xformular

    sel = ""
    sub = ''
    minle = ''
    maxle = ''
    miv = ''
    mav = ''

    _minle = ''
    _maxle = ''
    _minv = ''
    _maxv = ''
    _type = ''
    _size = ''


    if(select=='true'):
        sel="ja"
    else:
        sel=""

    if(subtype=='' or subtype==None ):
        sub=''
    else:
        sub = subtype

    if(minlength=='' or minlength==None ):
        minle=''
    else:
        minle = minlength

    if(maxlength=='' or maxlength==None ):
        maxle=''
    else:
        maxle = maxlength

    if(minvalue=='' or minvalue==None ):
        miv=''
    else:
        miv = minvalue

    if(maxvalue=='' or maxvalue==None ):
        mav=''
    else:
        mav = maxvalue

#-----------------------------------------

    try:
        _minle = attrs['minlength']
    except:
        _minle = ''

    try:
        _maxle = attrs['maxlength']
    except:
        _maxle = ''



    try:
        _minv = attrs['minvalue']
    except:
        _minv = ''

    try:
        _maxv = attrs['maxvalue']
    except:
        _maxv = ''

    try:
        _type = attrs['type']
    except:
        _type = ''

    try:
        _size = attrs['size']
    except:
        _size = ''





    if(element.tag_name == "select"):   # select durch option ersetzten
        tag = "option"
    else:

        tag = element.tag_name






    print(" %-4s  %-8s  %-8s  %-6s  %-6s  %-6s  %-6s  %-6s          %-8s  %-6s  %-6s  %-6s" % (id, type, sub,minle, maxle, sel,miv,mav,    tag,_type,_maxle,_size))
    return (id, type, subtype,minlength, maxlength, select,minvalue,maxvalue)

def OpenFile():
    filename = askopenfilename(initialdir="C:/Users/jp/Downloads/",
                           filetypes =(("XML Glump, vareckts", "*.xml"),("Des Glump brauch i ned","*.*")),
                           title = "Choose a file."
                           )
    print (filename)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        return(filename)
        # sys.stdout.flush()
    except:
        print("No file exists")


def find_type(id):
    element_id = id
    xmlns = "{http://www.govos.de/xsd/xformular2}"
    model = root.findall('%smodel' % (xmlns))  # R¸ckgabe ->Liste

    for g in model[0].iter():
        id = g.get('id')
        if (id == element_id):  # string vergleichen
            type = g.get('type')
            subtype = g.get('subtype')
            minlength = g.get('minLength')
            maxlength = g.get('maxLength')
            select = g.get('select')
            maxvalue = g.get('maxValue')
            minvalue = g.get('minValue')

            return(id,type,subtype,minlength,maxlength,select,minvalue,maxvalue)


def Klick(_xpath,show_info):
    try:
        elem = driver.find_element_by_xpath(_xpath)
        elem.click()
        time.sleep(delay)
        if(show_info):
            print(driver.current_url, driver.title)
            print(" %-4s  %-8s  %-8s  %-6s  %-6s  %-6s  %-6s  %-6s          %-8s  %-6s  %-6s  %-6s  " % ("id", "type", "subtype","minL", "maxL", "Liste", "minV", "maxV",    "tag","type",'maxL',"size"))
    except:
        pass

def weiter():
    try:
        elem = driver.find_element_by_xpath("//input[@value='weiter >']") # weiter button existiert
        if(elem):
            return True
    except:
        return False

def send_user(_xpath,show_info,text):
    elem = driver.find_element_by_xpath(_xpath)
    elem.send_keys(text)
    elem.send_keys(Keys.TAB)
    time.sleep(delay)
    if(show_info):
        print(driver.current_url, driver.title)


def fillpage():
    all_div_inputs =  driver.find_elements_by_class_name("xf2-field-input")  # alle Eingabefelder der Seite
    for div in all_div_inputs:                                               # aktuelles eingabefeld der Seite
        textarea = ""
        all_inputs = ""
        options = ""
        try:
            all_inputs = div.find_elements_by_tag_name('input')              # ein <input>   oder  mehrere  <input>s
        except:
            pass
        try:
            textarea = div.find_element_by_tag_name('textarea')              # null oder ein <textarea>
        except:
            pass
        try:
            options = div.find_elements_by_tag_name('option')                # mehrere  <option>
        except:
            pass

        if(len(all_inputs) != 0):                        # <input> vorhanden
            if(len(all_inputs)>1):                       #  mehr als 1 <input>  radio
                for input in all_inputs:
                    (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(input)
                    input.click()
            else:                                        #   1 <input>
                (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(all_inputs[0])

                if(type == 'string'):                                        # string
                    if(subtype == ''):                     #  ''
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("w"*randint(5, 11))
                        if(minlength):
                            all_inputs[0].send_keys("w" * int(minlength))
                        if (maxlength):
                            all_inputs[0].send_keys("w" * int(maxlength))
                    elif (subtype == None):                 # None
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("w"*randint(5, 11))
                        if (minlength):
                            all_inputs[0].send_keys("w" * int(minlength))
                        if (maxlength):
                            all_inputs[0].send_keys("w" * int(maxlength))
                    elif(subtype == 'plz'):                # plz
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("22234")
                    elif (subtype == 'email'):             # email
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("MisterX@mag-keinen-spam.de")
                    elif (subtype == 'bic'):               # bic
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("BYLADEM1001")
                    elif (subtype == 'iban'):             # iban
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("DE02120300000000202051")

                elif(type == 'integer'):                                       # integer
                    if (select == None):                   # None
                        if(maxlength != None):
                            value = "1" * int(maxlength)
                            value = str(value)
                        else:
                            value="1"
                        all_inputs[0].clear()
                        all_inputs[0].send_keys(value)
                    elif (select == ''):            # ''
                        if(maxlength != None):
                            value = "1" * int(maxlength)
                            value = str(value)
                        else:
                            value="1"
                        all_inputs[0].clear()
                        all_inputs[0].send_keys(value)
                    elif (select == 'true'):        # Liste
                        all_inputs[0].clear()
                        all_inputs[0].send_keys(1)
                elif(type == 'file'):                                         # file
                    pass
                elif(type == 'date'):                                         # date
                    global datum
                    all_inputs[0].clear()
                    js='arguments[0].value="'
                    js=js+str(datum)
                    js=js+'"'
                    # js = 'arguments[0].value="2019-01-21"'
                    driver.execute_script(js,all_inputs[0])
                    datum = datum + td
                elif (type == 'bool'):                                         # bool
                    all_inputs[0].click()
                else:
                    pass


        if(textarea):  # <textarea> vorhanden
            (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(textarea)
            textarea.clear()
            textarea.send_keys("aaaaaaaaaaaaaaaaaaaaaaa")

        if (len(options) != 0):  # <option> vorhanden
            for option in options:
                padre = option.find_element_by_xpath("..")
                (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(padre)
                option.click()
                pass





dateiname = OpenFile()
tree = ET.parse(dateiname)
root = tree.getroot()
driver = webdriver.Firefox()
driver.get(login)
send_user("//input[@name='username']",True,user)
time.sleep(10)
driver.execute_script("window.open('');")# Open a new window This does not change focus to the new window for the driver.
driver.switch_to.window(driver.window_handles[1])# Switch to the new window
driver.get(url1)
Klick("//input[@value='Weiter >']", True)  # Weiter button
check_eve()                                # check auf  Einverst‰ndniserkl‰rung
Klick("//a[@class='icon jp-button']", True)  # Assistent starten  button
i=0
check_eve()
while(weiter()):
    datum = date.today() - timedelta(9)
    fillpage()
    if(check_error()):
        print()
        print("FEHLERMELDUNG: ")
        print(check_error())
        break
    Klick("//input[@value='weiter >']", True)  # weiter button
    i += 1
    if(i == 31):
        break

# close the active tab
# driver.close()
# Switch back to the first tab
# driver.switch_to.window(driver.window_handles[0])
# Close the only tab, will also close the browser.
# driver.close()
# driver.get("https://www.govos-test.de/govos-test/portal/zs/875/vverfassung/164_1_5?p=3")
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button







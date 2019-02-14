from selenium import webdriver
import time
from datetime import date,timedelta
from selenium.webdriver.common.keys import Keys
import re
import xml.etree.ElementTree as ET
from tkinter.filedialog import askopenfilename
from random import *

login = "https://www.govos-test.de/govos-test/portal/desktop/0/login" # Login govos test
# login ="https://govos-t.niedersachsen.de/govos/portal/desktop/0/login?cookietest=1549458814742"  # test niedersachsen'

# url1="https://www.govos-test.de/govos-test/go/a/301"   #AGV-0001-
# url1="https://www.govos-test.de/govos-test/go/a/233"   # gewo 26
url1="https://www.govos-test.de/govos-test/go/a/288"     # gewo 21
# url1="https://govos-t.niedersachsen.de/govos/go/a/5"     #sta002
# url1="https://www.govos-test.de/govos-test/go/a/139"     #  uvg 001
# url1="https://www.govos-test.de/govos-test/go/a/342"     # i6ulza

delay=0.1
user=""
# pages=0
# first_page=""
td = timedelta(1)
ansehen_link = "//span[contains(text(),'ansehen/drucken')]"
show_info = True           # Schalter  Anzeige Infos
ids_to_variate = []        # IDs die variiert werden Vorauss. maxValue muss einen Wert haben (xformular.xml)

items_per_id = []          # wieviele Clicks pro ID maximal
all_test_cases = []



def ciralli_ansehen(xpath_ansehen):
    try:
        ciralli_hijo = driver.find_element_by_xpath("//span[contains(text(),'ansehen/drucken')]")
        if (ciralli_hijo):  # Einverständniserklärung
            ciralli_padre = ciralli_hijo.find_element_by_xpath("..")
            ciralli_padre.click()

    except:
        pass



def create_test_cases(a,i,lista):
    global all_test_cases
    elem = a[i]
    list_number_of_clicks = range(1,elem[1]+1)
    ID = elem[0]

    for clicks in list_number_of_clicks:

        tupla=(ID,clicks)
        lista1 = lista.copy()
        lista1.append(tupla)

        if (i+1 < len(a)):
            create_test_cases(a,i+1,lista1)
        else:
            # print(lista1)
            all_test_cases.append(lista1)


def calculate_items_per_id():         # Beispiel  items_per_id = [(19,2),(22,7)......]
    global items_per_id
    for id_to_variate in ids_to_variate:
        (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = find_type(str(id_to_variate))
        if(type == "bool"):
            items_per_id.append( (id_to_variate,2) )
        elif (type == "integer" and select == "true") :
            items_per_id.append((id_to_variate, int(maxvalue)))

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
    global show_info
    try:
        eve = driver.find_element_by_name("agreedchecked")
        if (eve):                                   # Einverständniserklärung

            eve.click()
            Klick("//input[@value='zustimmen']",show_info)
    except:
        pass



def log(element,show):
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

    if(show):
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
    model = root.findall('%smodel' % (xmlns))  # Rückgabe ->Liste

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


def Klick(_xpath,show):
    global delay
    try:
        elem = driver.find_element_by_xpath(_xpath)
        elem.click()
        time.sleep(delay)
        if(show):
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
    global delay
    elem = driver.find_element_by_xpath(_xpath)
    elem.send_keys(text)
    elem.send_keys(Keys.TAB)
    time.sleep(delay)
    if(show_info):
        print(driver.current_url, driver.title)


def fillpage(click_list=[]):
    global show_info,td
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

                (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(all_inputs[0], False)

                if(type == "integer"):                                                       # radios mit integer type
                    if(int(id) in ids_to_variate):    # input id   ist in id-Liste
                        for input in all_inputs:
                            (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(input, show_info)
                            for tupel in click_list:
                                if (id == str(tupel[0])):
                                    value = input.get_attribute("value")
                                    if (value == str(tupel[1])):   # wenn richtiger radio gefunden -> klick
                                        input.click()
                    else:                             # input id nicht in id Liste
                        (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(all_inputs[0], show_info)  # nur für log Ausgabe
                        for input in all_inputs:
                            value = input.get_attribute("value")
                            if (value == "1"):
                                input.click()
                else:                                                                             # radios mit bool type
                    if (int(id) in ids_to_variate):  # input id   ist in id-Liste
                        for input in all_inputs:
                            (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(input, show_info)

                            for tupel in click_list:
                                if (id == str(tupel[0])):
                                    value = input.get_attribute("value")
                                    erg="true"
                                    if(tupel[1] == 1):
                                        erg = "true"
                                    if (tupel[1] == 2):
                                        erg = "false"

                                    if (value == erg):  # wenn richtiger radio gefunden -> klick
                                        input.click()
                    else:                           # input id nicht in id Liste
                        (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(all_inputs[0],show_info)  # nur für log Ausgabe

                        for input in all_inputs:
                            value = input.get_attribute("value")
                            if (value == "true"):
                                input.click()


            else:                                        #   1 <input>
                (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(all_inputs[0],show_info)

                if(type == 'string'):                                                  # string
                    if(subtype == ''):                                   #  ''
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("w"*randint(5, 11))
                        if(minlength):
                            all_inputs[0].clear()
                            all_inputs[0].send_keys("i" * int(minlength))
                        if (maxlength):
                            all_inputs[0].clear()
                            all_inputs[0].send_keys("i" * int(maxlength))
                    elif (subtype == None):                              # None
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("w"*randint(5, 11))
                        if (minlength):
                            all_inputs[0].clear()
                            all_inputs[0].send_keys("i" * int(minlength))
                        if (maxlength):
                            all_inputs[0].clear()
                            all_inputs[0].send_keys("i" * int(maxlength))
                    elif(subtype == 'plz'):                              # plz
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("3" * randint(5, 11))
                        if (minlength):
                            all_inputs[0].clear()
                            all_inputs[0].send_keys("2" * int(minlength))
                        if (maxlength):
                            all_inputs[0].clear()
                            all_inputs[0].send_keys("3" * int(maxlength))
                    elif (subtype == 'email'):                           # email
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("MisterX@mag-keinen-spam.de")
                    elif (subtype == 'bic'):                              # bic
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("BYLADEM1001")
                    elif (subtype == 'iban'):                            # iban
                        all_inputs[0].clear()
                        all_inputs[0].send_keys("DE02120300000000202051")

                elif(type == 'integer'):                                               # integer
                    if (select == None):                                # None
                        if(maxlength != None):
                            value = "1" * int(maxlength)
                            value = str(value)
                        else:
                            value="1"
                        all_inputs[0].clear()
                        all_inputs[0].send_keys(value)
                    elif (select == ''):                                # ''
                        if(maxlength != None):
                            value = "1" * int(maxlength)
                            value = str(value)
                        else:
                            value="1"
                        all_inputs[0].clear()
                        all_inputs[0].send_keys(value)
                    elif (select == 'true'):                            # Liste
                        all_inputs[0].clear()
                        all_inputs[0].send_keys(1)
                elif(type == 'file'):                                                    # file        no functionality
                    pass
                elif(type == 'date'):                                                    # date
                    global datum
                    all_inputs[0].clear()
                    js='arguments[0].value="'
                    js=js+str(datum)
                    js=js+'"'
                    # js = 'arguments[0].value="2019-01-21"'
                    driver.execute_script(js,all_inputs[0])
                    datum = datum + td
                elif (type == 'bool'):                                                   # bool  -> checkbox
                    all_inputs[0].click()
                else:
                    pass


        if(textarea):  # <textarea> vorhanden
            (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(textarea,show_info)
            textarea.clear()
            textarea.send_keys("aaaaaaaaaaaaaaaaaaaaaaa")



        if (len(options) != 0):  # <option> vorhanden

            padre = options[0].find_element_by_xpath("..")
            (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(padre, False)

            if (type == "integer"):                                           # options mit integer type

                padre = options[0].find_element_by_xpath("..")
                (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(padre, False)
                if(int(id) in ids_to_variate):                # option id   ist in id-Liste
                    for option in options:
                        padre = option.find_element_by_xpath("..")
                        (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(padre, show_info)
                        for tupel in click_list:
                            if (id == str(tupel[0])):  # aktuelle option id  und  aktuelle tupel id sind gleich
                                value = option.get_attribute("value")
                                if (value == str(tupel[1])):
                                    option.click()
                else:                                          # option id   nicht  in id-Liste
                    padre = options[0].find_element_by_xpath("..")
                    (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(padre, show_info)  # nur für log Ausgabe
                    for option in options:
                        value = option.get_attribute("value")
                        if(value == "1"):
                            option.click()


            else:                                                                 # options mit bool type
                padre = options[0].find_element_by_xpath("..")
                (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(padre, False)
                if (int(id) in ids_to_variate):  # option id   ist in id-Liste
                    for option in options:
                        padre = option.find_element_by_xpath("..")
                        (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(padre, show_info)

                        for tupel in click_list:
                            if (id == str(tupel[0])):  # aktuelle option id  und  aktuelle tupel id sind gleich
                                value = option.get_attribute("value")
                                erg = "true"
                                if (tupel[1] == 1):
                                    erg = "true"
                                if (tupel[1] == 2):
                                    erg = "false"

                                if (value == erg):  # wenn richtiger option  gefunden -> klick
                                    option.click()


                else:                                # option id   nicht  in id-Liste
                    padre = options[0].find_element_by_xpath("..")
                    (id, type, subtype, minlength, maxlength, select, minvalue, maxvalue) = log(padre,show_info)  # nur für log Ausgabe

                    for option in options:
                        value = option.get_attribute("value")
                        if (value == "true"):
                            option.click()


def xfomular_laden():
    global dateiname
    global tree
    global root

    dateiname = OpenFile()
    tree = ET.parse(dateiname)
    root = tree.getroot()

def starten():
    global ids_to_variate , items_per_id , driver ,user ,url1,show_info,all_test_cases,ansehen_link,login
    if(len(ids_to_variate)==0):  # keine Varianten
        pass
    else:
        calculate_items_per_id()
        print(" items per ID " ,items_per_id)
        create_test_cases(items_per_id,0,[])
        for x in all_test_cases:
            print(x)

    driver = webdriver.Firefox()
    driver.get(login)
    send_user("//input[@name='username']",True,user)
    time.sleep(10)


    if(len(ids_to_variate)==0):    # keine Varianten
        driver.execute_script(
            "window.open('');")  # Open a new window This does not change focus to the new window for the driver.
        driver.switch_to.window(driver.window_handles[1])  # Switch to the new window
        driver.get(url1)
        Klick("//input[@value='Weiter >']", show_info)  # Weiter button
        check_eve()  # check auf  Einverständniserklärung
        Klick("//a[@class='icon jp-button']", show_info)  # Assistent starten  button
        i = 0
        check_eve()
        while (weiter()):

            datum = date.today() - timedelta(9)
            fillpage()
            if (check_error()):
                print()
                print("FEHLERMELDUNG: ")
                print(check_error())
                break
            Klick("//input[@value='weiter >']", show_info)  # weiter button
            i += 1
            if (i == 31):
                break
        ciralli_ansehen(ansehen_link)

    else:
        for x in range(1,len(all_test_cases)+1):
            driver.execute_script("window.open('');")# Open a new window This does not change focus to the new window for the driver.
            driver.switch_to.window(driver.window_handles[x])# Switch to the new window
            driver.get(url1)
            Klick("//input[@value='Weiter >']", show_info)  # Weiter button
            check_eve()                                # check auf  Einverständniserklärung
            Klick("//a[@class='icon jp-button']", show_info)  # Assistent starten  button
            i=0
            check_eve()
            while(weiter()):

                datum = date.today() - timedelta(9)
                fillpage(all_test_cases[x-1])
                if(check_error()):
                    print()
                    print("FEHLERMELDUNG: ")
                    print(check_error())
                    break
                Klick("//input[@value='weiter >']", show_info)  # weiter button
                i += 1
                if(i == 31):
                    break
            ciralli_ansehen(ansehen_link)


# close the active tab
# driver.close()
# Switch back to the first tab
# driver.switch_to.window(driver.window_handles[0])
# Close the only tab, will also close the browser.
# driver.close()
# Klick("//input[@value='weiter >']",True) # weiter button
# Klick("//input[@value='weiter >']",True) # weiter button







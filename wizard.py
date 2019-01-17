import xml.etree.ElementTree as ET
import re
import os
from tkinter.filedialog import askopenfilename
# from ElementTree_pretty import prettify

def dump_element():
    print('dump  !')
    element_id = input('ID ?')
    xmlns = "{http://www.govos.de/xsd/xformular2}"
    wizard = root.findall('%swizard' % (xmlns))  # Rückgabe ->Liste

    for g in wizard[0].iter():
        id = g.get('id')
        if (id == element_id):  # string vergleichen
            ET.dump(g)


def clear_screen():
    os.system('cls')

def view_element():
    print("view element !")
    str_auswahl = input('ID ?')
    aa = "_" * 34
    bb = "-   "*9
    print(aa)
    xmlns = "{http://www.govos.de/xsd/xformular2}"
    wizard = root.findall('%swizard' % (xmlns))  # Rückgabe ->Liste
    for g in wizard[0].iter():
        name = g.get('name')
        id = g.get('id')
        if (id == str_auswahl):
            # print("%-8s%15s" % ( id,name))
            print("%-10s%-20s%4s" % ((re.split('^{.+}', g.tag))[1], name, id))

            print(bb)
            print("%-10s%-20s%4s" % ('tag', 'name', 'id'))
            print("%-10s%-20s%4s" % ('---', '----', '--'))

            subelements = g.findall('*')
            for sub in subelements:
                try:
                    name_sub = sub.get('name')
                    if (name_sub == None):
                        name_sub="x"
                except:
                    name_sub="x"
                try:
                    id_sub = sub.get('id')
                    if (id_sub == None):
                        id_sub="x"
                except:
                    id_sub="x"

                try:
                    text_sub = (sub.text).strip()
                except:
                    text_sub = ""

                print("%-10s%-20s%4s" % (  (re.split('^{.+}',sub.tag))[1]  , name_sub, id_sub))
    print(aa)





def nextID_as_int(root):
    next = int((root.find('{http://www.govos.de/xsd/xformular2}wizard')).get('nextId'))
    return next



def show_wizard_elements():
    wizard = root.findall('{http://www.govos.de/xsd/xformular2}wizard')
    aa="*"*34
    print(aa)
    print("%-10s%-20s%4s" % ('tag', 'name', 'id'))
    print("%-10s%-20s%4s" % ('---', '----', '--'))

    for g in wizard[0]:
        name = g.get('name')
        # print( "%-20s  %-20s  %-4s" % ( id(g),name,g.get('id') )  )
        print( "%-10s%-20s%4s" % ((re.split('^{.+}',g.tag))[1], name,g.get('id') )  )
    print(aa)

def show_sub_wizard_elements():
    aa="_"*34
    bb = "--  "*9
    pages = root.findall('{http://www.govos.de/xsd/xformular2}wizard/{http://www.govos.de/xsd/xformular2}page')  # Rückgabe ->Liste
    for g in pages:
        name = g.get('name')
        id = g.get('id')
        print(aa)
        # print("%-8s%15s" % ( str(id),name))
        print("%-10s%-20s%4s" % ((re.split('^{.+}', g.tag))[1], name, id))
        print(bb)
        print("%-10s%-20s%4s" % ('tag', 'name', 'id'))
        print("%-10s%-20s%4s" % ('---', '----', '--'))
        subelements = g.findall('*')
        for sub in subelements:
            try:
                name_sub = sub.get('name')
                if (name_sub == None):
                    name_sub="x"
            except:
                name_sub="x"
            try:
                id_sub = int(sub.get('id'))
            except:
                id_sub="x"

            try:
                text_sub = (sub.text).strip()
            except:
                text_sub = ""

            print("%-10s%-20s%4s" % (  (re.split('^{.+}',sub.tag))[1]  , name_sub, id_sub))
    print(aa)

def show_rows():
    aa = "_" * 34
    bb = "--  " * 9
    pages = root.findall(
        '{http://www.govos.de/xsd/xformular2}wizard/{http://www.govos.de/xsd/xformular2}page')  # Rückgabe ->Liste
    for g in pages:
        name = g.get('name')
        id = g.get('id')
        print(aa)
        # print("%-8s%15s" % ( str(id),name))
        print("%-10s%-20s%4s" % ((re.split('^{.+}', g.tag))[1], name, id))
        print(bb)
        print("%-10s%-20s%4s" % ('tag', 'field', 'id'))
        print("%-10s%-20s%4s" % ('---', '----', '--'))
        subelements = g.findall('{http://www.govos.de/xsd/xformular2}rows')
        for sub in subelements:
            fields=sub.findall('{http://www.govos.de/xsd/xformular2}field')
            for field in fields:
                try:
                    name_sub = field.get('field')
                    if (name_sub == None):
                        name_sub = "x"
                except:
                    name_sub = "x"
                try:
                    id_sub = int(field.get('id'))
                except:
                    id_sub = "x"

                try:
                    text_sub = (field.text).strip()
                except:
                    text_sub = ""

                print("%-10s%-20s%4s" % ((re.split('^{.+}', field.tag))[1], name_sub, id_sub))
    print(aa)

def del_all_subIDs(gruppe):
    alle_IDs=[]
    for element in gruppe.iter():
        try:
            if(element.attrib['id']):
                # alle_IDs.append(int(element.attrib['id']))
                del element.attrib['id']
        except:
            pass
    # print('folgende IDs werden gelöscht')
    # print(alle_IDs)
    # ET.dump(gruppe)

def copy_element():
    auswahl = int(input('copy  ID  ? '))
    wohin = int(input('insert after ID  ? '))
    wieoft = int(input('how many times ? '))
    counter = int(input('start with counter   ? '))

    str_auswahl = str(auswahl)
    str_wohin = str(wohin)

    xmlns = "{http://www.govos.de/xsd/xformular2}"
    wizard = root.findall('%swizard' % (xmlns))  # Rückgabe ->Liste
    for kopie in wizard[0].iter():
        if(kopie.get('id')==str_auswahl):
            break
    pos=0

    for parent in wizard[0].iter():
        pos=0
        for ziel in parent:
            if(ziel.get('id')==str_wohin):
                break
            pos+=1
        else:
            continue
        break

    while wieoft:
        nodestr = ET.tostring(kopie)   # kopie in string
        parent.insert(pos+1,ET.XML(nodestr))   # kopie einfügen , string wieder einlesen sonst ist es nur eine Referenz auf kopie

        next = nextID_as_int(root)          # nextID holen
        del_all_subIDs(parent[pos+1])
        parent[pos+1].set('id',str(next))  # id von neuer gruppe auf nextId setzten

        name1 = parent[pos+1].get('name')   # name von neuer Gruppe
        links = (re.split('_\d+$',name1))[0]     #  aufteilen in links = hauptname  und rechts = fortlaufende nummer  Format='_3'
        parent[pos+1].set('name', (links+'_'+str(wieoft+counter-1)))

        next+=1
        root[0].set('nextId',str(next))        # nextId hochzählen
        wieoft -= 1


def delete_element():
    print('delete element !')
    auswahl=int(input('which ID  ?'))
    str_auswahl = str(auswahl)
    xmlns = "{http://www.govos.de/xsd/xformular2}"
    wizard =  root.findall('%swizard'%(xmlns))  # Rückgabe ->Liste

    for parent in wizard[0].iter():
        for child in parent:
            id = child.get('id')
            if(id==str_auswahl):    #  string vergleichen
                parent.remove(child)


def change_name():
    print('change name  !')
    str_auswahl = input('ID ?')
    change = input('new Name ?')
    xmlns = "{http://www.govos.de/xsd/xformular2}"
    wizard = root.findall('%swizard' % (xmlns))  # Rückgabe ->Liste

    for g in wizard[0].iter():
        id =g.get('id')
        if (id == str_auswahl):     # string vergleichen
                g.set('name',change)

def OpenFile():
    filename = askopenfilename(initialdir="C:/Users/jp/Downloads/",
                           filetypes =(("XML Glump, vareckts", "*.xml"),("Des Glump brauch i ned","*.*")),
                           title = "Choose a file."
                           )
    print (filename)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        return(filename)
        sys.stdout.flush()
    except:
        print("No file exists")


# OpenFile()
# tree = ET.parse('AGV-006-NI-FL.xf2.xml')
# tree = ET.parse('test.xml')

# root = tree.getroot()
# next = nextID_as_int(root)
# show_wizard_elements()

while(1):
    was = input('1:open   2:change   3:del   4:copy   5:view   6:wizard    7:cls   8:dump  9:rows\n ')

    if was == '9':
        show_rows()
    elif was == '8':
        dump_element()
    elif was == '7':
        clear_screen()
        show_wizard_elements()
    elif was == '6':
        show_sub_wizard_elements()
    elif was == '5':
        view_element()
    elif was == '4':
        copy_element()
    elif was == '3':
        delete_element()
    elif was == '2':
        change_name()
    elif was == '1':
        global tree
        global root
        dateiname = OpenFile()
        tree = ET.parse(dateiname)
        root = tree.getroot()
        show_wizard_elements()

    else:

        print(" - Got a false expression value")

tree.write('test.xml')

# gruppe_kopieren()
# change_name()
# delete_element()
# show_wizard_elements()
# next = nextID_as_int(root)
# print('next ID = {0}'.format(next))
# tree.write('test.xml')













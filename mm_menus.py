# !/usr/bin/env python

import os.path as check
import gobject
import gtk
from gtk import gdk
import gmenu

CATICONSPATHS=["/usr/share/icons/gnome/32x32/categories/"]
APPICONSPATH="/usr/share/icons/hicolor/48x48/apps/"
ALTICONSPATH=["/usr/share/icons/hicolor/32x32/apps/", "/usr/share/pixmaps/",
              "/usr/share/icons/gnome/48x48/apps/", "/usr/share/icons/gnome/32x32/apps/",
              "/usr/share/icons/hicolor/24x24/apps/", "/usr/share/icons/gnome/32x32/devices/"]

class MenuDateStore:
    MENUCORE = gmenu.lookup_tree('applications.menu')
    MENUROOT = MENUCORE.get_root_directory()
    SYSTEMMENUCORE = gmenu.lookup_tree('settings.menu')
    SYSTEMMENUROOT = SYSTEMMENUCORE.get_root_directory()
    PATH = []

def set_model(treeview,lst,theme,location_icon):
    """
    This item produces a complete model from a treeview,
    a model base, and a list
    """
    model = gtk.ListStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING)
    for row in lst:
        try:
            if '/' in row[0]:
                if check.exists(row[0]) == True:
                    row[0] = gdk.pixbuf_new_from_file (row[0])
                else:row[0] = gdk.pixbuf_new_from_file (location_icon)
            elif '.' in row[0] and '/' not in row[0]:
                location = "/usr/share/pixmaps/" + row[0]
                if check.exists(location) == True:
                    row[0] = gdk.pixbuf_new_from_file (location)
                else:row[0] = gdk.pixbuf_new_from_file (location_icon)
            elif row[0] == None:
                row[0] = gdk.pixbuf_new_from_file (location_icon)
            else:
                row[0] = theme.load_icon(row[0],48,0)
        except:
            row[0] = gdk.pixbuf_new_from_file (location_icon)

        try:
            if 48 != row[0].get_height():
                row[0] = row[0].scale_simple(48,48,gtk.gdk.INTERP_BILINEAR)
        except:
            print row[0]
        model.append(row)
    return model

def get_menus(root,root2=None):
    """
    returns a list of menus from root and root2
    """
    listall = []
    listobj = {}
    for menu in root.contents:
        if menu.get_type() == gmenu.TYPE_SEPARATOR:pass
        elif menu.get_type() == gmenu.TYPE_DIRECTORY:
            name = menu.get_name()
            #if len(name) >= 21:
            #    name = name[:21] + '...'
            lst = []
            lst.append(menu.get_icon())
            lst.append(name)
            listall.append(lst)
            listobj[name] = [2,menu]
        elif menu.get_type() == gmenu.TYPE_ENTRY:
            name = menu.get_name()
            #if len(name) >= 21:
            #    name = name[:21] +'..'
            lst = []
            lst.append(menu.get_icon())
            lst.append(name)
            listall.append(lst)
            listobj[name] = [1,menu.exec_info]
    if root2 != None:
        for menu in root2.contents:
            if menu.get_type() == gmenu.TYPE_SEPARATOR:pass
            elif menu.get_type() == gmenu.TYPE_DIRECTORY:
                name = menu.get_name()
                #if len(name) >= 21:
                #    name = name[:21] +'...'
                lst = []
                lst.append(menu.get_icon())
                lst.append(name)
                listall.append(lst)
                listobj[name] = [2,menu]
            elif menu.get_type() == gmenu.TYPE_ENTRY:
                name = menu.get_name()
                #if len(name) >= 21:
                #    name = name[:21] + '...'
                lst = []
                lst.append(menu.get_icon())
                lst.append(name)
                listall.append(lst)
                listobj[name] = [1,menu.exec_info]
    return listall,listobj

def clean_icon_path(path):
    if '/' in path:
        return path
    else:
        if 'png' not in path:
            path = path + '.png'
        if check.exists(APPICONSPATH+path) == True:
            return APPICONSPATH+path
        else:
            for p in ALTICONSPATH:
                if check.exists(p+path) == True:
                    return p+path
    return 'keepass.png'

def clean_cat_path(cat):
    if check.exists(cat) == True:
        return cat
    else:
        return 'keepass.png'

def getAll():
    menu_order = []
    menu_dict = {}

    data = MenuDateStore()
    lst1, cat_map = get_menus( data.MENUROOT, root2=data.SYSTEMMENUROOT )
    for i in lst1:
        menu_order.append(i[1])
        menu_dict[i[1]] = {'icon': i[0], 'items': []}
        lst2, short_map = get_menus(cat_map[i[1]][1])
        subitems = []
        for s in lst2:
            ticon = clean_icon_path(s[0])
            title = formatTitle(s[1])
            temp = {'icon':ticon,'title':title,'command':short_map[s[1]][1]}
            subitems.append(temp)
        menu_dict[i[1]]['items'] = subitems
    return menu_dict, menu_order

def formatTitle(text):
    return text
    if len(text) < 16:
        return text
    else:
        b = []
        t = text.split()
        cr = ''
        for i in t:
            if len(cr) + len(i) < 16:
                cr += i+' '
            else:
                b.append(cr)
                cr = i
        return b


if __name__ == '__main__':
    print getAll()
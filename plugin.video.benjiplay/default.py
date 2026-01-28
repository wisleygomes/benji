# -*- coding: utf-8 -*-

import sys
import xbmcgui
import xbmcplugin

addon_handle = int(sys.argv[1])
base_url = sys.argv[0]
params = sys.argv[2][1:]

def build_url(action):
    return base_url + "?action=" + action

def add_dir(name, action, icon=""):
    li = xbmcgui.ListItem(label=name)
    if icon:
        li.setArt({"icon": icon, "thumb": icon})
    li.setInfo("video", {"title": name})
    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=build_url(action),
        listitem=li,
        isFolder=True
    )

def main_menu():
    add_dir("🎬 Filmes", "filmes")
    add_dir("📺 Séries", "series")
    add_dir("📡 TV Ao Vivo", "aovivo")
    xbmcplugin.endOfDirectory(addon_handle)

def filmes():
    xbmcgui.Dialog().notification(
        "Benji Play",
        "Área de filmes em desenvolvimento",
        xbmcgui.NOTIFICATION_INFO,
        3000
    )

def series():
    xbmcgui.Dialog().notification(
        "Benji Play",
        "Área de séries em desenvolvimento",
        xbmcgui.NOTIFICATION_INFO,
        3000
    )

def aovivo():
    xbmcgui.Dialog().notification(
        "Benji Play",
        "TV ao vivo em breve",
        xbmcgui.NOTIFICATION_INFO,
        3000
    )

def router(paramstring):
    if paramstring == "":
        main_menu()
    elif "action=filmes" in paramstring:
        filmes()
    elif "action=series" in paramstring:
        series()
    elif "action=aovivo" in paramstring:
        aovivo()
    else:
        main_menu()

if __name__ == "__main__":
    router(params)
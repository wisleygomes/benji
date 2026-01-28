# -*- coding: utf-8 -*-

import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import os

addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')

ICON = os.path.join(addon_path, 'icon.png')
FANART = os.path.join(addon_path, 'fanart.jpg')

def add_item(name, action):
    url = sys.argv[0] + "?action=" + action
    li = xbmcgui.ListItem(label=name)

    li.setInfo("video", {"title": name})
    li.setArt({
        "icon": ICON,
        "thumb": ICON,
        "fanart": FANART
    })

    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=url,
        listitem=li,
        isFolder=True
    )

def router(paramstring):
    if paramstring == "":
        show_menu()
    else:
        xbmcgui.Dialog().ok("Benji Play", "Opção ainda em desenvolvimento")

def show_menu():
    add_item("📺 Filmes", "filmes")
    add_item("🎬 Séries", "series")
    add_item("📡 Ao Vivo", "aovivo")
    xbmcplugin.endOfDirectory(addon_handle)

if __name__ == "__main__":
    params = sys.argv[2][1:]
    router(params)
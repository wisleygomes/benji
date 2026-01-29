# -*- coding: utf-8 -*-

import sys
import os
import xbmcgui
import xbmcplugin
import xbmcaddon

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
    li.setProperty("IsPlayable", "false")

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
        xbmcgui.Dialog().ok(
            "Benji Play 😎",
            "Conteúdo em desenvolvimento eterno.\n\nVolte em 2035."
        )

def show_menu():
    add_item("📺 Filmes", "filmes")
    add_item("🎬 Séries", "series")
    add_item("📡 Ao Vivo", "aovivo")
    xbmcplugin.endOfDirectory(addon_handle)

if __name__ == "__main__":
    params = sys.argv[2][1:]
    router(params)

    # -*- coding: utf-8 -*-

import sys
import requests
import xbmcgui
import xbmcplugin

addon_handle = int(sys.argv[1])
base_url = sys.argv[0]

M3U_URL = "https://iptv-org.github.io/iptv/index.m3u"

def build_url(query):
    return base_url + "?" + query

def main_menu():
    li = xbmcgui.ListItem(
        label="📡 IPTV – Lista Pública",
    )
    li.setArt({
        "icon": "special://home/addons/plugin.video.benjiplay/icon.png",
        "fanart": "special://home/addons/plugin.video.benjiplay/fanart.jpg"
    })

    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=build_url("action=iptv"),
        listitem=li,
        isFolder=True
    )

    xbmcplugin.endOfDirectory(addon_handle)

def load_m3u():
    response = requests.get(M3U_URL, timeout=15)
    lines = response.text.splitlines()

    name = None
    for line in lines:
        if line.startswith("#EXTINF"):
            name = line.split(",", 1)[1]
        elif line.startswith("http"):
            li = xbmcgui.ListItem(label=name)
            li.setInfo("video", {"title": name})
            li.setArt({
                "icon": "special://home/addons/plugin.video.benjiplay/icon.png",
                "fanart": "special://home/addons/plugin.video.benjiplay/fanart.jpg"
            })
            xbmcplugin.addDirectoryItem(
                handle=addon_handle,
                url=line,
                listitem=li,
                isFolder=False
            )

    xbmcplugin.endOfDirectory(addon_handle)

def router(paramstring):
    if paramstring == "":
        main_menu()
    elif "action=iptv" in paramstring:
        load_m3u()

if __name__ == "__main__":
    params = sys.argv[2][1:]
    router(params)
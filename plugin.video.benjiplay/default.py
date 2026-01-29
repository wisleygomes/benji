# -*- coding: utf-8 -*-

import sys
import os
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests

addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')

ICON = os.path.join(addon_path, 'icon.png')
FANART = os.path.join(addon_path, 'fanart.jpg')

M3U_URL = "https://iptv-org.github.io/iptv/index.m3u"

# =========================
# UTIL
# =========================
def build_url(query):
    return sys.argv[0] + "?" + query

# =========================
# MENU PRINCIPAL
# =========================
def show_menu():
    add_folder("📺 Filmes", "filmes")
    add_folder("🎬 Séries", "series")
    add_folder("📡 Ao Vivo (IPTV)", "iptv")
    xbmcplugin.endOfDirectory(addon_handle)

def add_folder(name, action):
    li = xbmcgui.ListItem(label=name)
    li.setInfo("video", {"title": name})
    li.setArt({
        "icon": ICON,
        "thumb": ICON,
        "fanart": FANART
    })
    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=build_url("action=" + action),
        listitem=li,
        isFolder=True
    )

# =========================
# IPTV (M3U)
# =========================
def load_iptv():
    try:
        response = requests.get(M3U_URL, timeout=15)
        lines = response.text.splitlines()
    except Exception as e:
        xbmcgui.Dialog().notification(
            "Benji Play",
            "Erro ao carregar IPTV",
            xbmcgui.NOTIFICATION_ERROR
        )
        return

    name = None
    for line in lines:
        if line.startswith("#EXTINF"):
            name = line.split(",", 1)[1]
        elif line.startswith("http"):
            li = xbmcgui.ListItem(label=name)
            li.setInfo("video", {"title": name})
            li.setArt({
                "icon": ICON,
                "thumb": ICON,
                "fanart": FANART
            })
            li.setProperty("IsPlayable", "true")

            xbmcplugin.addDirectoryItem(
                handle=addon_handle,
                url=line,
                listitem=li,
                isFolder=False
            )

    xbmcplugin.endOfDirectory(addon_handle)

# =========================
# ROUTER
# =========================
def router(paramstring):
    if paramstring == "":
        show_menu()
    elif "action=iptv" in paramstring:
        load_iptv()
    else:
        xbmcgui.Dialog().ok(
            "Benji Play 😎",
            "Conteúdo ainda em desenvolvimento."
        )

# =========================
# START
# =========================
if __name__ == "__main__":
    params = sys.argv[2][1:]
    router(params)
# -*- coding: utf-8 -*-

import sys
import requests
import xbmcgui
import xbmcplugin
import re

addon_handle = int(sys.argv[1])
base_url = sys.argv[0]

ICON = os.path.join(addon_path, 'icon.png')
FANART = os.path.join(addon_path, 'fanart.jpg')


M3U_URL = "https://iptv-org.github.io/iptv/index.m3u"

COUNTRIES = {
    "BR": "🇧🇷 Brasil",
    "US": "🇺🇸 Estados Unidos",
    "PT": "🇵🇹 Portugal",
    "ES": "🇪🇸 Espanha"
}

def build_url(query):
    return base_url + "?" + query

def main_menu():
    add_dir("📺 Filmes", "filmes")
    add_dir("🎬 Séries", "series")
    add_dir("📡 IPTV", "iptv")
    xbmcplugin.endOfDirectory(addon_handle)

def add_dir(name, action):
    li = xbmcgui.ListItem(label=name)
    li.setArt({
        "icon": "special://home/addons/plugin.video.benjiplay/icon.png",
        "fanart": "special://home/addons/plugin.video.benjiplay/fanart.jpg"
    })
    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=build_url(f"action={action}"),
        listitem=li,
        isFolder=True
    )

def iptv_menu():
    for code, name in COUNTRIES.items():
        li = xbmcgui.ListItem(label=name)
        li.setArt({
            "icon": "special://home/addons/plugin.video.benjiplay/icon.png",
            "fanart": "special://home/addons/plugin.video.benjiplay/fanart.jpg"
        })
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=build_url(f"action=channels&country={code}"),
            listitem=li,
            isFolder=True
        )
    xbmcplugin.endOfDirectory(addon_handle)

def load_channels(country_code):
    response = requests.get(M3U_URL, timeout=20)
    lines = response.text.splitlines()

    name = None
    country = None

    for line in lines:
        if line.startswith("#EXTINF"):
            name = line.split(",", 1)[1]
            match = re.search(r'tvg-country="([^"]+)"', line)
            country = match.group(1) if match else None
        elif line.startswith("http") and country == country_code:
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
        iptv_menu()
    elif "action=channels" in paramstring:
        country = paramstring.split("country=")[-1]
        load_channels(country)
    else:
        xbmcgui.Dialog().ok("Benji Play", "Em desenvolvimento")

if __name__ == "__main__":
    params = sys.argv[2][1:]
    router(params)
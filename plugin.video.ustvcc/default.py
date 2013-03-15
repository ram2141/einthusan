# Einthusan.com plugin written by humla.

import os
import re
import urllib, urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
from t0mm0.common.net import Net

ADDON = xbmcaddon.Addon(id='plugin.video.ustvcc')

def http_get(url):
    net = Net()
    try:
        return net.http_GET(url).content.encode("utf-8")
    except urllib2.URLError, e:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to connect to website', '', '') 
        return ""

def http_post(url, post_data):
    net = Net()
    try:
        return net.http_POST(url, post_data).content.encode("utf-8")
    except urllib2.URLError, e:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to connect to website', '', '') 
        return ""   

##
# Prints the main categories. Called when id is 0.
##
def main_categories(name, url):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    url = 'http://www.ustv.cc/episode/'

    addDir('A-Z', url, 3, '')
    addDir('Hot TV Series', '', 7, '')
    addDir('Latest Updates TV Series', '', 8, '')
    addDir('New TV Episodes', '', 8, '')
    #addDir('Favourites', '', 8, '')
    #addDir('Search', '', 6, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def a_z_view(name, url):
    azlist = map (chr, range(97,122))

    addDir('Numerical', url + 'num.htm', 5, '')

    for letter in azlist:
        addDir(letter, url + letter + '.htm', 5, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))   

def list_hot_TV_series (name, url):
    url = 'http://ustv.cc/episode/Arrow.htm'
    html = http_get(url)
    matches = re.compile('<span class="jumu"><a title=".+?" href="(/episode/(.+?).htm)">(.+?)</a></span><span class="nabe">(.+?)</span>').findall(html)

    BASE_URL = "http://ustv.cc"
    for link, base_name, name, clicks in matches:
        addDir(name + " : [COLOR red]" + clicks + " clicks [/COLOR]", BASE_URL + link, 1, get_icon_url(base_name))    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))    

##
# Shows a list of Tv series. Called when mode is 5.
##
def list_tv_series_list(name, url):
    html = http_get(url)
    list_tv_series_list_aux(html)

def list_tv_series_list_aux(html):
    bulk = re.compile('<dl class="list_wut">((.|\n)+?)</dl>').findall(html)

    if (len(bulk) > 0):
        matches = re.compile('title=".+?" href="(/episode/(.+?).htm)">(.+?)</a>').findall(bulk[len(bulk) - 1][0])
        BASE_URL = "http://ustv.cc"
        for link, base_name, name in matches:
            addDir(name, BASE_URL + link, 1, get_icon_url(base_name))
        xbmcplugin.endOfDirectory(int(sys.argv[1]))    
    else:
        # Display a dialog
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Cant get any TV Series', '', '') 

#
# List the seasons for a specific TV series. Called when mode is 1.
#
def list_seasons(name, url):
    html = http_get(url)
    matches = re.compile(' <label  id=".+?".+?onclick="selecttab\(\'(.+?)\'\)" ').findall(html)

    img = re.compile('<img.+?src="(.+?)"').findall(html)
    image = ''
    if (len(img) > 0):
        image = img[0]

    for season in matches:
        addDir("Season " + season, url, 4, image)  
    xbmcplugin.endOfDirectory(int(sys.argv[1]))    

# Lists all the episdoes in the given season.
# Called when mode is 4
#
def list_episodes_in_season(name, url):
    season_number = name.split(' ', 1)[1]
    tab = "stab" + season_number

    html = http_get(url)
    compile_string = '<ul class="ju_list" id="' + tab + '"((.|\\n)+?)</ul>'
    bulk = re.compile(compile_string).findall(html)

    if (len(bulk) > 0):
        img = re.compile('<img.+?src="(.+?)"').findall(html)
        image = ''
        if (len(img) > 0):
            image = img[0]

        matches = re.compile('<a href="(.+?)">(.+?)</a>').findall(bulk[0][0])
        BASE_URL = "http://www.ustv.cc"
        for link, name in matches:
            addDir(name, BASE_URL + link, 2, image)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))    
    else:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Cant find any episodes', '', '') 

# Displays the list of new tv series.
# Called when mode is 8
def list_latest_update_tv_series(name, url):
    BASE_URL = "http://ustv.cc"
    html = http_get(BASE_URL)

    bulk = re.compile('<div class="hot_aes">' + name + '</div>((.|\n)+?)</ul>').findall(html)

    if (len(bulk) > 0):
        matches = re.compile('<a title=".+? " href="(/episode/(.+?).htm)">(.+?)</a>.+?color="#FF0000">(.+?)</font>').findall(bulk[0][0])
        IMG_BASE = "http://d.ustv.cc/img/%s.jpg"
        for link, base_name, name, ep in matches:
            ep = ep.replace('&nbsp;','')
            addDir(name + ":[COLOR red]" + ep +"[/COLOR]", BASE_URL + link, 1, get_icon_url(base_name))
        xbmcplugin.endOfDirectory(int(sys.argv[1]))    
    else:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Cannot find TV series', '', '') 

def get_icon_url(base_name):
    IMG_BASE = "http://d.ustv.cc/img/%s.jpg"
    if (base_name.count('-') > 1):
        base_name = base_name.replace('-','.')
    base_name = base_name.replace("\'","")
    return IMG_BASE%base_name

##
# Shows the search box for serching. Shown when the id is 6.
##
def show_search_box(name, url):
    search_term = urllib.quote_plus(GUIEditExportName(""))
    search_url = 'http://ustv.cc/s.php'

    post_data = {}
    post_data['kw']=search_term

    html =  http_post(search_url, post_data)
    list_tv_series_list_aux(html)
    

##
# Plays the video. Called when the id is 2.
#
##
def play_video(name, url):
    html =  http_get(url)

    print html
    match = re.compile('[\'\"].+?\?key=(.+?)[\"\']').findall(html)

    print match

    if (len (match) > 0):
        key = 'http://d.ustv.cc/ip.mp4?key=' + urllib.quote(match[0])

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        listitem = xbmcgui.ListItem(name)
        playlist.add(key, listitem)
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
    else:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Cannot find a video stream', '', '') 


##
# Displays the setting view. Called when mode is 12
##
def display_setting(name, url, language, mode):
    ADDON.openSettings()

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

#########################################################
# Function  : GUIEditExportName                         #
#########################################################
# Parameter :                                           #
#                                                       #
# name        sugested name for export                  #
#                                                       # 
# Returns   :                                           #
#                                                       #
# name        name of export excluding any extension    #
#                                                       #
#########################################################
def GUIEditExportName(name):
    exit = True 
    while (exit):
          kb = xbmc.Keyboard('default', 'heading', True)
          kb.setDefault(name)
          kb.setHeading("Enter the search term")
          kb.setHiddenInput(False)
          kb.doModal()
          if (kb.isConfirmed()):
            name_confirmed  = kb.getText()
            name_correct = name_confirmed.count(' ')
            name = name_confirmed
            exit = False
          else:
            GUIInfo(2,__language__(33225)) 
    return(name)

def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok


def addDir(name, url, mode, iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable', 'true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok


            
params=get_params()
url=None
name=None
mode=0

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass

try:
    name=urllib.unquote_plus(params["name"])
except:
    pass

try:
    mode=int(params["mode"])
except:
    pass


# Modes
# 0: The main Categories Menu. Selection of language
# 1: For scraping the movies from a list of movies in the website
# 2: For playing a video
# 3: The Recent Section
# 4: The top viewed list. like above
# 5: The top rated list. Like above
# 6: Search options
# 7: Sub menu
# 8: A-Z view.
# 9: Yearly view
# 10: Actor view
# 11: Director view
# 12: Show Addon Settings

function_map = {}
function_map[0] = main_categories
function_map[1] = list_seasons
function_map[2] = play_video
function_map[3] = a_z_view
function_map[4] = list_episodes_in_season
function_map[5] = list_tv_series_list
function_map[6] = show_search_box
function_map[7] = list_hot_TV_series
function_map[8] = list_latest_update_tv_series



function_map[mode](name, url)
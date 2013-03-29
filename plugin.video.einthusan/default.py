# Einthusan.com plugin written by humla.

import os
import re
import urllib, urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
from t0mm0.common.net import Net

ADDON = xbmcaddon.Addon(id='plugin.video.einthusan')

def http_get(url, login=False):
    # Dont need cookies right now..
    #cookie_file = create_cookie_file()
    net = Net()
    if login:
        login_url = "http://www.einthusan.com/etc/login.php"

        username = xbmcplugin.getSetting(int(sys.argv[1]), 'username')
        password = xbmcplugin.getSetting(int(sys.argv[1]), 'password')

        if (username != '' and password != ''):
            form_data = {}
            form_data['username'] = username
            form_data['password'] = password
            try:
                net.http_POST(login_url, form_data)
            except urllib2.URLError, e:
                xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to login to website', '', '') 
    try:
        return net.http_GET(url).content
    except urllib2.URLError, e:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to connect to website', '', '') 
        return ""


def create_cookie_file():
    try:
        ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
        cookie_file = os.path.join(ADDON_USERDATA_FOLDER, 'cookies')
        if not os.path.exists(cookie_file):
            print "Creating the cookie file"
            open(cookie_file,'w').close()
        return cookie_file
    except:
        return cookie_file

##
# Prints the main categories. Called when id is 0.
##
def main_categories(name, url, language, mode):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    addDir('Hindi', '', 7, img_path + '/Hindi_Movies.png', 'hindi')
    addDir('Tamil', '', 7,img_path + '/Tamil_Movies.png', 'tamil')
    addDir('Telugu', '', 7, img_path + '/Telugu_Movies.png', 'telugu')
    addDir('Malayalam', '', 7, img_path + '/Malayalam_Movies.png', 'malayalam')
    addDir('Addon Settings', '', 12, '', '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows categories for each language
##
def inner_categories(name, url, language, mode, bluray=False): 

    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    base_url = 'http://www.einthusan.com/movies/'
    if bluray:
        base_url = 'http://www.einthusan.com/bluray/'

    addDir('A-Z', base_url, 8, '', language)
    addDir('Years', base_url, 9, '', language)
    addDir('Actors', base_url, 10,'', language)
    addDir('Director', base_url, 11,'', language)
    addDir('Recent', base_url, 3,'', language)
    addDir('Top Rated', base_url, 5, '', language)
    if not bluray:
        addDir('Featured', '', 4,'', language)
        addDir('Blu-Ray', '', 13, img_path + '/Bluray.png', language)
        addDir('Search', '', 6, img_path + '/Search_by_title.png', language)
        addDir('Music Video', '' , 14, '', language)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
#  Displays the categories for Blu-Ray
#
def display_BluRay_listings(name, url, language, mode):
    inner_categories(name, url, language, mode, True)

##
#  Scrapes a list of movies and music videos from the website. Called when mode is 1.
##
def get_movies_and_music_videos(name, url, language, mode):
    html =  http_get(url)
    match = re.compile('<div class="(video|music)-object-thumb"><a href="(.+?)">(.+?<a class="movie-cover-wrapper".+?>)?<img src="(.+?)" alt="(.+?)"').findall(html)

    # Bit of a hack
    MOVIES_URL = "http://www.einthusan.com/movies/"
    for _, page_link, _, image, name in match:
        if (mode == 1):
            image = MOVIES_URL + image
        addDir(name, MOVIES_URL + page_link, 2, image, image)

    numerical_nav = re.compile('<div class="numerical-nav">(.+?)</div>').findall(html)

    if (len(numerical_nav) > 0):
        next_page = re.compile('<a class="numerical-nav-selected" href=".+?">.+?</a><a href=".+?">(.+?)</a>').findall(numerical_nav[0])
        if (len(next_page) == 1):
            addDir("Next >>", url + "&page=" + next_page[0], mode, "http://www.sahara.co.za/Images/next.jpg", '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
#  Just displays the two recent sections. Called when id is 3.
#
##
def show_recent_sections(name, url, language, mode):
    INDEX_URL = url + 'index.php?organize=Activity&org_type=Activity&page=1&lang='+language

    addDir('Recently Posted', INDEX_URL + '&filtered=RecentlyPosted', 1, '', '')
    addDir('Recently Viewed', INDEX_URL + '&filtered=RecentlyViewed', 1, '', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows the sections for Top Viewed. Called when id is 4.
#  ******* The website has dropped this *******************
##
def show_top_viewed_options(name, url, language, mode):
    INDEX_URL = url + 'index.php?organize=Statistics&org_type=Statistics&page=1&lang='+language

    addDir('All Time', INDEX_URL + '&filtered=AllTimeViews' , 1, '', '')
    addDir('This Week', INDEX_URL + '&filtered=ThisWeekViews', 1, '', '')
    addDir('Last Week', INDEX_URL + '&filtered=LastWeekViews', 1, '', '')
    addDir('This Month', INDEX_URL + '&filtered=ThisMonthViews', 1, '', '')
    addDir('Last Month', INDEX_URL + '&filtered=LastMonthViews' , 1, '', '')
    addDir('This Year', INDEX_URL + '&filtered=ThisYearViews' , 1, '', '')
    addDir('Last Year', INDEX_URL + '&filtered=LastYearViews' , 1, '', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Shows the movie in the homepage..
def show_featured_movies(name, url, language, mode):
    page_url = 'http://www.einthusan.com/index.php?lang=' + language
    html = http_get(page_url)
    matches = re.compile('<a class="movie-cover-wrapper" href="(.+?)"><img src="(.+?)" alt="(.+?)" ').findall(html)

    BASE_URL = 'http://www.einthusan.com/'
    for link, image, name in matches:
        addDir(name, BASE_URL + link, 2, BASE_URL + image, language)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


##
# Displays the options for Top Rated. Called when id is 5.
##
def show_top_rated_options(name, url, language, mode):
    INDEX_URL = url + 'index.php?organize=Rating&org_type=Rating&page=1&lang=' + language

    addDir('Romance', INDEX_URL + '&filtered=Romance', 1, '')
    addDir('Comedy', INDEX_URL + '&filtered=Comedy', 1, '')
    addDir('Action', INDEX_URL + '&filtered=Action', 1, '')
    addDir('Storyline', INDEX_URL + '&filtered=Storyline', 1, '')
    addDir('Performance', INDEX_URL + '&filtered=Performance', 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


##
# Displays the options for A-Z view. Called when id is 8.
##
def show_A_Z(name, url, language, mode):
    azlist = map (chr, range(65,91))

    INDEX_URL = url + 'index.php?organize=Alphabetical&org_type=Alphabetical&lang='+language

    addDir('Numerical', INDEX_URL + '&filtered=Numerical', 1, '')

    for letter in azlist:
        addDir(letter, INDEX_URL + '&filtered=' + letter, 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
##
# Single method that shows the list of years, actors and directors. 
# Called when id is 9, 10, 11
# 9 : List of Years
# 10: List of Actors
# 11: List of directors
## 
def show_list(name, b_url, language, mode):

    url = b_url + 'index.php?organize=Director'
    if (mode == 9):
        url = b_url + 'index.php?organize=Year'
    elif (mode == 10):
        url = b_url + 'index.php?organize=Cast'
    url = url + "&lang="+language

    BASE_URL = b_url + 'index.php'
    
    html =  http_get(url)

    list_div = re.compile('<div class="video-organizer-element-wrapper">(.+?)</div>').findall(html)

    if len(list_div) > 0:
        years = re.compile('<a href="(.+?)">(.+?)</a>').findall(list_div[0])

        for year_url,year in years:
            addDir(year, BASE_URL + year_url, 1, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows the search box for serching. Shown when the id is 6.
##
def show_search_box(name, url, language, mode):
    search_term = GUIEditExportName("")

    search_url = 'http://www.einthusan.com/search/?search_query=' + search_term + "&lang=" + language

    html =  http_get(search_url)

    match = re.compile('<a href="(../movies/watch.php.+?)">(.+?)</a>').findall(html)

    # Bit of a hack again
    MOVIES_URL = "http://www.einthusan.com/movies/"

    for url,name in match:
        addDir(name, MOVIES_URL + url, 2, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
#  Displays a list of music videos
##
def list_music_videos(name, url, language, mode):
    if (url == "" or url == None):
        url = 'http://www.einthusan.com/music/index.php?lang=' + language 
    get_movies_and_music_videos(name, url, language, mode)
##
# Plays the video. Called when the id is 2.
#
##
def play_video(name, url, language, mode):
    html =  http_get(url, True)
    match = re.compile("'hd-2': { 'file': '(.+?)'").findall(html)

    if (len(match) == 0):
        match = re.compile("'file': '(.+?)'").findall(html)

    # Bit of a hack again
    MOVIES_URL = "http://www.einthusan.com/movies/"

    image_link = language
    if (image_link == ""):
        thumbnail_match = re.compile('<img src="(../images.+?)"').findall(html)
        if (len (thumbnail_match) > 0):
            image_link = MOVIES_URL + thumbnail_match[0]

    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    if (len (match) > 0):
        listitem = xbmcgui.ListItem(name)
        if (image_link != ""):
            listitem.setThumbnailImage(image_link)
        playlist.add(urllib.unquote(match[0]), listitem)
    xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)

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
              if (name_correct):
                 GUIInfo(2,__language__(33224)) 
              else: 
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


def addDir(name, url, mode, iconimage, lang=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&lang="+urllib.quote_plus(lang)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable', 'true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok


            
params=get_params()
url=None
name=None
mode=0
language=None

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

try:
    language=urllib.unquote_plus(params["lang"])
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
function_map[1] = get_movies_and_music_videos
function_map[2] = play_video
function_map[3] = show_recent_sections
function_map[4] = show_featured_movies
function_map[5] = show_top_rated_options
function_map[6] = show_search_box
function_map[7] = inner_categories
function_map[8] = show_A_Z
function_map[9] = show_list
function_map[10] = show_list
function_map[11] = show_list
function_map[12] = display_setting
function_map[13] = display_BluRay_listings
function_map[14] = list_music_videos

function_map[mode](name, url, language, mode)
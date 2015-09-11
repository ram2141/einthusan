# Einthusan.com plugin written by humla.

import os
import re
import urllib, urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
from datetime import date

import HTTPInterface
import JSONInterface
import DBInterface

ADDON = xbmcaddon.Addon(id='plugin.video.einthusan')

##
# Prints the main categories. Called when id is 0.
##
def main_categories(name, url, language, mode):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 
    addDir('Hindi', '', 7, img_path + 'Hindi_Movies.png', 'hindi')
    addDir('Tamil', '', 7,img_path + 'Tamil_Movies.png', 'tamil')
    addDir('Telugu', '', 7, img_path + 'Telugu_Movies.png', 'telugu')
    addDir('Malayalam', '', 7, img_path + 'Malayalam_Movies.png', 'malayalam')
    addDir('Kannada', '', 7, img_path + 'kannada.jpg', 'kannada')
    addDir('Bengali', '', 7, img_path + 'movie.png', 'bengali')
    addDir('Marathi', '', 7, img_path + 'movie.png', 'marathi')
    addDir('Punjabi', '', 7, img_path + 'movie.png', 'punjabi')
    addDir('Addon Settings', '', 12, img_path + 'settings.png', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows categories for each language
##
def inner_categories(name, url, language, mode, bluray=False): 
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    postData = 'lang=' + language + '&'
    if bluray:
        postData = 'lang=' + language + '&bluray=1&'

    addDir('A-Z', postData, 8, img_path + 'a_z.png', language)
    addDir('Years', postData, 9, img_path + 'years.png', language)
    addDir('Actors', postData, 10, img_path + 'actors.png', language)
    addDir('Director', postData, 11, img_path + 'director.png', language)
    addDir('Recent', postData, 3, img_path + 'recent.png', language)
    addDir('Top Rated', postData, 5, img_path + 'top_rated.png', language)
    if not bluray:
        addDir('Featured', '', 4, img_path + 'featured_videos.png', language)
        addDir('Blu-Ray', '', 13, img_path + 'Bluray.png', language)
        addDir('Search', postData, 6, img_path + 'Search_by_title.png', language)
        addDir('Music Video', '' , 14, img_path + 'music_videos.png', language)
        #addDir('Mp3 Music', '', 16, '', language)
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
    ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    COOKIE_FILE = os.path.join(ADDON_USERDATA_FOLDER, 'cookies')

    html =  HTTPInterface.http_get(url, cookie_file=COOKIE_FILE)
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
# Displays the menu for mp3 music..
# Called when id is 16
## 
def mp3_menu(name, url, language, mode):
    #addDir('')
    return 1

##
# Make a post request to the JSON API and list the movies..
# Interacts with the other interfaces..
##
def list_movies_from_JSON_API(name, url, language, mode):
    # HACK: Used "url" to transport postData because we know the API url
    #       and dont need it here.
    postData = url
    response = JSONInterface.apply_filter(postData)

    if ('results' in response):
        movie_ids = response['results']

        bluray = False
        if (url.find('bluray') > -1):
            bluray = True
        add_movies_to_list(movie_ids, bluray)

        max_page = int(response['max_page']) 
        next_page = int(response['page']) + 1

        if (next_page <= max_page):
            cwd = ADDON.getAddonInfo('path')
            img_path = cwd + '/images/next.png' 
            addDir("[B]Next Page[/B] >>>", url + "&page=" + str(next_page), mode, img_path)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def add_movies_to_list(movie_ids, bluray):
    ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    DB_FILE = os.path.join(ADDON_USERDATA_FOLDER, 'movie_info_cache.db')

    COVER_BASE_URL = 'http://www.einthusan.com/images/covers/'
    if (bluray):
        BASE_URL = 'http://www.einthusan.com/movies/watch.php?bluray=true&id='
    else:
        BASE_URL = 'http://www.einthusan.com/movies/watch.php?id='
    for m_id in movie_ids:
        movie_info = DBInterface.get_cached_movie_details(DB_FILE, m_id)
        if (movie_info == None):
            _, name, image = JSONInterface.get_movie_detail(m_id)
            if (image == None):
                image = ''
            DBInterface.save_move_details_to_cache(DB_FILE, m_id, name, image)
        else:
            _, name, image = movie_info
        addDir(name, BASE_URL + str(m_id) ,2, COVER_BASE_URL + image)

##
#  Just displays the two recent sections. Called when id is 3.
##
def show_recent_sections(name, url, language, mode):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    postData = url + '&organize=Activity&filtered='
    addDir('Recently Posted',  postData + 'RecentlyPosted', 15, img_path + 'recently_added.png')
    addDir('Recently Viewed', postData + 'RecentlyViewed', 15, img_path + 'recently_viewed.png')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Shows the movie in the homepage..
def show_featured_movies(name, url, language, mode):
    page_url = 'http://www.einthusan.com/index.php?lang=' + language

    ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    COOKIE_FILE = os.path.join(ADDON_USERDATA_FOLDER, 'cookies')
    html = HTTPInterface.http_get(page_url, cookie_file = COOKIE_FILE)
    matches = re.compile('<a class="movie-cover-wrapper" href="(.+?)"><img src="(.+?)" alt="(.+?)" ').findall(html)

    BASE_URL = 'http://www.einthusan.com/'
    for link, image, name in matches:
        addDir(name, BASE_URL + link, 2, BASE_URL + image, language)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the options for Top Rated. Called when id is 5.
##
def show_top_rated_options(name, url, language, mode):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    postData = url + '&organize=Rating&filtered='
    addDir('Romance', postData + 'Romance', 15, img_path + 'romance.png')
    addDir('Comedy', postData + 'Comedy', 15, img_path + 'comedy.png')
    addDir('Action', postData + 'Action', 15, img_path + 'action.png')
    addDir('Storyline', postData + 'Storyline', 15, img_path + 'storyline.png')
    addDir('Performance', postData + 'Performance', 15, img_path + 'performance.png')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the options for A-Z view. Called when id is 8.
##
def show_A_Z(name, url, language, mode):
    azlist = map (chr, range(65,91))
    postData = url + "&organize=Alphabetical&filtered="
    addDir('Numerical', postData + 'Numerical', 15, '')
    for letter in azlist:
        addDir(letter, postData + letter, 15, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Single method that shows the list of years, actors and directors. 
# Called when id is 9, 10, 11
# 9 : List of Years
# 10: List of Actors
# 11: List of directors
## 
def show_list(name, b_url, language, mode):
    if (mode == 9):
        try:
            postData = b_url + 'organize=Year'
            values = JSONInterface.get_year_list(language)
        except:
            # build default list of years
            values = [repr(x) for x in reversed(range(1950, date.today().year + 1))]
    elif (mode == 10):
        postData = b_url + 'organize=Cast'
        values = JSONInterface.get_actor_list(language)
    else:
        postData = b_url + 'organize=Director'
        values = JSONInterface.get_director_list(language)

    postData = postData + '&filtered='

    for attr_value in values:
        if (attr_value != None):
            addDir(attr_value, postData + attr_value, 15, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows the search box for serching. Shown when the id is 6.
##
def show_search_box(name, url, language, mode):
    search_term = GUIEditExportName("")
    postData = url + 'search=' + search_term
    list_movies_from_JSON_API(name, postData, language, 15)

##
#  Displays a list of music videos
##
def list_music_videos(name, url, language, mode):
    if (url == "" or url == None):
        url = 'http://www.einthusan.com/music/index.php?lang=' + language 
    get_movies_and_music_videos(name, url, language, mode)

def http_request_with_login(url):
    username = xbmcplugin.getSetting(int(sys.argv[1]), 'username')
    password = xbmcplugin.getSetting(int(sys.argv[1]), 'password')

    ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    COOKIE_FILE = os.path.join(ADDON_USERDATA_FOLDER, 'cookies')
    return HTTPInterface.http_get(url, COOKIE_FILE,username, password)

##
# Plays the video. Called when the id is 2.
##
def play_video(name, url, language, mode):
    print "Playing: " + name + ", with url:"+ url
    html =  http_request_with_login(url)
    match = re.compile("'hd-2': { 'file': '(.+?)'").findall(html)

    if (len(match) == 0):
        match = re.compile("'file': '(.+?)'").findall(html)

    image_link = language
    if (image_link == ""):
        thumbnail_match = re.compile('<img src="(../images.+?)"').findall(html)
        if (len (thumbnail_match) > 0):
            # Bit of a hack again
            MOVIES_URL = "http://www.einthusan.com/movies/"
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
              name = kb.getText()
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
url=''
name=''
mode=0
language=''

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
function_map[15] = list_movies_from_JSON_API
function_map[16] = mp3_menu

function_map[mode](name, url, language, mode)
# Einthusan.com plugin written by humla.

import re
import urlresolver
import urllib,urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
from t0mm0.common.net import Net


def GA():
    from random import randint
    from urllib import urlencode
    from urllib2 import urlopen
    from urlparse import urlunparse
    from hashlib import sha1
    from os import environ
    PROPERTY_ID = environ.get("GA_PROPERTY_ID", "UA-38297897")

    # Generate the visitor identifier somehow. I get it from the
    # environment, calculate the SHA1 sum of it, convert this from base 16
    # to base 10 and get first 10 digits of this number.
    VISITOR = environ.get("GA_VISITOR", "xxxxx")
    VISITOR = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]

    # The path to visit
    PATH = "xbmc_einthusan"

    # Collect everything in a dictionary
    DATA = {"utmwv": "4.2.8-FRODO",
            "utmn": str(randint(1, 9999999999)),
            "utmp": PATH,
            "utmac": PROPERTY_ID,
            "utmcc": "__utma=%s;" % ".".join(["1", VISITOR, "1", "1", "1", "1"])}

    # Encode this data and generate the final URL
    URL = urlunparse(("http",
                      "www.google-analytics.com",
                      "/__utm.gif",
                      "",
                      urlencode(DATA),
                      ""))
    urlopen(URL).info()

##
# Prints the main categories. Called when id is 0.
##
def CATEGORIES():
    cwd = xbmcaddon.Addon().getAddonInfo('path')
    img_path = cwd + '/images/'

    addDir('Hindi', 'hindi', 7, '')
    addDir('Tamil', 'tamil', 7, '')
    #addDir('ChandraMukhi Tamil Movie (Bluray Preview)', 'http://www.einthusan.com/movies/watch.php?id=56&bluray=true', 2, '')
    addDir('Addon Settings', '', 12, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows categories for each language
##
def inner_categories(language): 
    addDir('A-Z', language, 8, '')
    addDir('Years', language, 9, '')
    addDir('Actors', language, 10,'')
    addDir('Director', language, 11,'')
    addDir('Recent', language, 3,'')
    addDir('Top Viewed', language, 4,'')
    addDir('Top Rated', language, 5,'')
    addDir('Search', language, 6, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
#  Scrapes a list of movies from the website. Called when mode is 1.
##
def INDEX(url):
    print "Getting video links"
    html = Net().http_GET(url).content

    match = re.compile('<a class="movie-cover-wrapper" href="(.+?)"><img src="(.+?)" alt="(.+?)"').findall(html)

    # Bit of a hack
    MOVIES_URL = "http://www.einthusan.com/movies/"
    for page_link,image,name in match:
        addDir(name, MOVIES_URL + page_link, 2, MOVIES_URL + image)


    numerical_nav = re.compile('<div class="numerical-nav">(.+?)</div>').findall(html)

    if (len(numerical_nav) > 0):
        next_page = re.compile('<a class="numerical-nav-selected" href=".+?">.+?</a><a href=".+?">(.+?)</a>').findall(numerical_nav[0])
        if (len(next_page) == 1):
            addDir("Next >>", url + "&page=" + next_page[0], 1, "http://www.sahara.co.za/Images/next.jpg")

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
#  Just displays the two recent sections. Called when id is 3.
#
##
def show_recent_sections(language):
    
    INDEX_URL = 'http://www.einthusan.com/movies/index.php?organize=Activity&org_type=Activity&page=1&lang='+language

    addDir('Recently Posted', INDEX_URL + '&filtered=RecentlyPosted', 1, '')
    addDir('Recently Viewed', INDEX_URL + '&filtered=RecentlyViewed', 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows the sections for Top Viewed. Called when id is 4.
#
##
def show_top_viewed_options(language):
    INDEX_URL = 'http://www.einthusan.com/movies/index.php?organize=Statistics&org_type=Statistics&page=1&lang='+language

    addDir('All Time', INDEX_URL + '&filtered=AllTimeViews' , 1, '')
    addDir('This Week', INDEX_URL + '&filtered=ThisWeekViews', 1, '')
    addDir('Last Week', INDEX_URL + '&filtered=LastWeekViews', 1, '')
    addDir('This Month', INDEX_URL + '&filtered=ThisMonthViews', 1, '')
    addDir('Last Month', INDEX_URL + '&filtered=LastMonthViews' , 1, '')
    addDir('This Year', INDEX_URL + '&filtered=ThisYearViews' , 1, '')
    addDir('Last Year', INDEX_URL + '&filtered=LastYearViews' , 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the options for Top Rated. Called when id is 5.
#
##
def show_top_rated_options(language):
    INDEX_URL = 'http://einthusan.com/movies/index.php?organize=Rating&org_type=Rating&page=1&lang=' + language

    addDir('Romance', INDEX_URL + '&filtered=Romance', 1, '')
    addDir('Comedy', INDEX_URL + '&filtered=Comedy', 1, '')
    addDir('Action', INDEX_URL + '&filtered=Action', 1, '')
    addDir('Storyline', INDEX_URL + '&filtered=Storyline', 1, '')
    addDir('Performance', INDEX_URL + '&filtered=Performance', 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


##
# Displays the options for A-Z view. Called when id is 8.
##
def show_A_Z(language):
    azlist = map (chr, range(65,91))

    INDEX_URL = 'http://www.einthusan.com/movies/index.php?organize=Alphabetical&org_type=Alphabetical&lang='+language

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
def show_list(language, mode):

    url = 'http://www.einthusan.com/movies/index.php?organize=Director'
    if (mode == 9):
        url = 'http://einthusan.com/movies/index.php?organize=Year'
    elif (mode == 10):
        url = 'http://www.einthusan.com/movies/index.php?organize=Cast'
    url = url + "&lang="+language

    BASE_URL = 'http://einthusan.com/movies/index.php'
    
    html = Net().http_GET(url).content

    list_div = re.compile('<div class="video-organizer-element-wrapper">(.+?)</div>').findall(html)

    if len(list_div) > 0:
        years = re.compile('<a href="(.+?)">(.+?)</a>').findall(list_div[0])

        for year_url,year in years:
            addDir(year, BASE_URL + year_url, 1, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows the search box for serching. Shown when the id is 6.
##
def show_search_box(language):
    search_term = GUIEditExportName("")

    search_url = 'http://www.einthusan.com/search/?search_query=' + search_term + "&lang=" + language

    html = Net().http_GET(search_url).content
    match = re.compile('<a href="(../movies/watch.php.+?)">(.+?)</a>').findall(html)

    # Bit of a hack again
    MOVIES_URL = "http://www.einthusan.com/movies/"

    for url,name in match:
        addDir(name, MOVIES_URL + url, 2, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#Function from xbmc.org forum. This is used to pop-up a virtual keyboard.
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
   
#########################################################

##
# Plays the video. Called when the id is 2.
#
##
def play_video(url,name):
    log("Playing " + name)
    log("Playing " + url)
    
    html = Net().http_GET(url).content

    match = re.compile("'hd-2': { 'file': '(.+?)'").findall(html)

    if (len(match) == 0):
        match = re.compile("'file': '(.+?)'").findall(html)

    thumbnail_match = re.compile('<img src="(../images.+?)"').findall(html)

    # Bit of a hack again
    MOVIES_URL = "http://www.einthusan.com/movies/"

    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    for stream_link in match:
        listitem = xbmcgui.ListItem(name)
        if (len(thumbnail_match) > 0):
            listitem.setThumbnailImage(MOVIES_URL+thumbnail_match[0])
        playlist.add(stream_link, listitem)
    player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    player.play(playlist)
    GA()

##
# Displays the setting view. Called when mode is 12
##
def display_setting():
    xbmcaddon.Addon(id='plugin.video.einthusan').openSettings()

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

def addLink(name,url,iconimage):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok


def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def log(message):
    print "[Eithusan] " + message
              
params=get_params()
url=None
name=None
mode=None

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

print "Mode: " + str(mode)
print "Name: " + str(name)
print "URL: " + str(url)

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

if mode==None: # or url==None or len(url)<1:
    CATEGORIES()
elif mode==1:
    INDEX(url)
elif mode==2:
    play_video(url,name)
elif mode==3:
    ## Here url is used to transport the language
    show_recent_sections(url)
elif mode==4:
    ## Here url is used to transport the language
    show_top_viewed_options(url)
elif mode==5:
    ## Here url is used to transport the language
    show_top_rated_options(url)
elif mode==6:
    ## Here url is used to transport the language
    show_search_box(url)
elif mode==7:
    ## Here url is used to transport the language
    inner_categories(url) 
elif mode==8:
    ## Here url is used to transport the lanuage
    show_A_Z(url)
elif mode in [9,10,11]:
    ## Here url is used to transport language
    show_list(url, mode)
elif mode==12:
    display_setting();

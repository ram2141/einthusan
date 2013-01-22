# Einthusan.com plugin written by humla.

import re
import os
import urlresolver
import urllib,urllib2
import xbmcplugin,xbmcgui
import xbmcaddon

# Taken from desitvforum xbmc plugin.
def GetDomain(url):
    print url
    tmp = re.compile('//(.+?)/').findall(url)
    domain = 'Unknown'
    if len(tmp) > 0:
        domain = tmp[0].replace('www.', '')
    return domain


##
# Prints the main categories. Called when id is 0.
##
def CATEGORIES():
    cwd = xbmcaddon.Addon().getAddonInfo('path')
    img_path = cwd + '/images/'

    addDir('Search', '', 6, '')
    
    addDir('Hindi', 'hindi', 7, '')
    addDir('Tamil', 'tamil', 7, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows categories for each language
##
def inner_categories(language): 
    addDir('A-Z', language, 8, '')
    addDir('Recent', language, 3,'')
    addDir('Top Viewed', language, 4,'')
    addDir('Top Rated', language, 5,'')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
#  Scrapes a list of movies from the website. Called when id is 1.
#
##
def INDEX(url):
    print "Getting video links"
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    # Bit of a hack
    MOVIES_URL = "http://www.einthusan.com/movies/"

    match = re.compile('<a class="movie-cover-wrapper" href="(.+?)"><img src="(.+?)" alt="(.+?)"').findall(link)

    for page_link,image,name in match:
        addDir(name, MOVIES_URL + page_link, 2, MOVIES_URL + image)

    next_page = re.compile('<a class="numerical-nav-selected" href=".+?">.+?</a><a href=".+?">(.+?)</a>').findall(link)

    if (len(next_page) == 1):
        addDir("Next >>", url + "&page=" + next_page[0], 1, "http://www.sahara.co.za/Images/next.jpg")
#
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
#  Just displays the two recent sections. Called when id is 3.
#
##
def show_recent_sections(language):
    
    INDEX_URL = 'http://www.einthusan.com/movies/index.php?'

    addDir('Recently Posted', INDEX_URL + 'organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=1&lang='+language, 1, '')
    addDir('Recently Viewed', INDEX_URL + 'organize=Activity&filtered=RecentlyViewed&org_type=Activity&page=1&lang='+language, 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows the sections for Top Viewed. Called when id is 4.
#
##
def show_top_viewed_options(language):
    INDEX_URL = 'http://www.einthusan.com/movies/index.php?'

    addDir('All Time', INDEX_URL + 'organize=Statistics&filtered=AllTimeViews&org_type=Statistics&page=1&lang=' + language, 1, '')
    addDir('This Week', INDEX_URL + 'organize=Statistics&filtered=ThisWeekViews&org_type=Statistics&page=1&lang=' + language, 1, '')
    addDir('Last Week', INDEX_URL + 'organize=Statistics&filtered=LastWeekViews&org_type=Statistics&page=1&lang='+ language, 1, '')
    addDir('This Month', INDEX_URL + 'organize=Statistics&filtered=ThisMonthViews&org_type=Statistics&page=1&lang='+ language, 1, '')
    addDir('Last Month', INDEX_URL + 'organize=Statistics&filtered=LastMonthViews&org_type=Statistics&page=1&lang=' + language, 1, '')
    addDir('This Year', INDEX_URL + 'organize=Statistics&filtered=ThisYearViews&org_type=Statistics&page=1&lang=' + language, 1, '')
    addDir('Last Year', INDEX_URL + 'organize=Statistics&filtered=LastYearViews&org_type=Statistics&page=1&lang=' + language, 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the options for Top Rated. Called when id is 5.
#
##
def show_top_rated_options(language):
    INDEX_URL = 'http://www.einthusan.com/movies/index.php?'

    addDir('Romance', INDEX_URL + 'organize=Rating&filtered=Romance&org_type=Rating&page=1&lang='+language, 1, '')
    addDir('Comedy', INDEX_URL + 'organize=Rating&filtered=Comedy&org_type=Rating&page=1&lang='+language, 1, '')
    addDir('Action', INDEX_URL + 'organize=Rating&filtered=Action&org_type=Rating&page=1&lang='+language, 1, '')
    addDir('Storyline', INDEX_URL + 'organize=Rating&filtered=Storyline&org_type=Rating&page=1&lang='+language, 1, '')
    addDir('Performance', INDEX_URL + 'organize=Rating&filtered=Performance&org_type=Rating&page=1&lang='+language, 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


##
# Displays the options for A-Z view. Called when id is 8.
##
def show_A_Z(language):
    azlist = map (chr, range(65,91))

    INDEX_URL = 'http://www.einthusan.com/movies/index.php?'

    addDir('Numerical', INDEX_URL + 'organize=Alphabetical&filtered=Numerical&org_type=Alphabetical&lang=' + language, 1, '')

    for letter in azlist:
        addDir(letter, INDEX_URL + 'organize=Alphabetical&org_type=Alphabetical&filtered=' + letter + '&lang=' + language, 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
##
# Displays the options for yearly view. Called when id is 9.
# To be implemented
##
def show_yearly_view(language):
    a = 1

##
# Shows the search box for serching. Shown when the id is 6.
##
def show_search_box():
    search_term = GUIEditExportName("")

    search_url = 'http://www.einthusan.com/search/?lang=hindi&search_query=' + search_term

    req = urllib2.Request(search_url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    match = re.compile('<a href="(../movies/watch.php.+?)">(.+?)</a>').findall(link)

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
    
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    match = re.compile("'hd-2': { 'file': '(.+?)'").findall(link)

    thumbnail_match = re.compile('<img src="(../images.+?)"').findall(link)

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
        show_search_box()
elif mode==7:
        ## Here url is used to transport the language
        inner_categories(url) 
elif mode==8:
        ## Here url is used to transport the lanuage
        show_A_Z(url)

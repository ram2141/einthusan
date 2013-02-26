import re
import os
import urllib,urllib2
import xbmcplugin,xbmcgui
import xbmcaddon
from t0mm0.common.net import Net

ADDON = xbmcaddon.Addon(id='plugin.video.desionlinetheater')
NAME = "DesiOnlineTheater"

# Taken from desitvforum xbmc plugin.
def GetDomain(url):
    tmp = re.compile('//(.+?)/').findall(url)
    domain = 'Unknown'
    if len(tmp) > 0:
        domain = tmp[0].replace('www.', '')
    return domain

def make_http_get(url):
    try:
        return Net().http_GET(url).content
    except:
        xbmcgui.Dialog().ok(NAME, 'Unable to connect to website', '', '') 
        return ""

########################### Start ###############################################


##   
##  http://www.sominaltvfilms.com/feeds/posts/summary/-/Trailer?max-results=10&alt=json-in-script
def list_latest_trailers():
    return False

##  http://www.sominaltvfilms.com/feeds/posts/summary/-/BluRay?max-results=10&alt=json-in-script
def list_latest_BluRay_releases():
    return False

##  http://www.sominaltvfilms.com/feeds/posts/summary/-/LDR?max-results=15&alt=json-in-script
##
def list_latest_DVD_releases():
    return False

def list_latest_movies():
    return False

def list_most_viewed_movies():
    return False

# Shows the different Categories
def initial_categories():
    addDir("HomePage" , "http://desionlinetheater.com/", 1, "")
    #addDir("Hindi", "http://www.bharathcinemas.info/category/watch-hindi-movies-online/",1, "")
    #addDir("Tamil", "http://www.bharathcinemas.info/category/watch-tamil-movies-online/",1, "")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Called when id is 
def list_homepage_options():
    addDir("Most Viewed", "", 2, "")
    addDir("Latest Movies", "", 3, "")
    addDir("Latest DVD Releases", "", 4, "")
    addDir("Latest BluRays", "", 4, "")
    addDir("Latest Trailers", "", 4, "")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))    
    return False


##################################################### Generic Stuff ###################

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
    print name
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok


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
# 0: The main Categories Menu
# 1:
# 2: For indexing movies from HomePage
# 3: For getting a list of video links

if mode==None or url==None or len(url)<1:
    initial_categories()
elif mode==1:
    list_homepage_options()
elif mode==2:
    list_most_viewed_movies()
elif mode==3:
    list_latest_movies()
elif mode==4:
    list_latest_DVD_releases()
elif mode==5:
    list_latest_BluRay_releases()
elif mode==6:
    list_latest_trailers()
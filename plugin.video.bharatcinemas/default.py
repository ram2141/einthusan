# CanadaNepal plugin written by humla.

import re
import os
import urlresolver
import urllib,urllib2
import xbmcplugin,xbmcgui
import xbmcaddon
from t0mm0.common.net import Net

ADDON = xbmcaddon.Addon(id='plugin.video.bharatcinemas')
NAME = "BharatCinemas"

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


# Shows the different Categories
def CATEGORIES():
    addDir("HomePage" , "http://www.bharathcinemas.info/", 2, "")
    addDir("Hindi", "http://www.bharathcinemas.info/category/watch-hindi-movies-online/",1, "")
    addDir("Tamil", "http://www.bharathcinemas.info/category/watch-tamil-movies-online/",1, "")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Shows the movies in the home_page
def index_homepage(url):
    html = make_http_get(url)

    matches = re.compile('class="small_thumb" src="(.+?)".+?\\nhref="(.+?)" title="(.+?)">').findall(html)

    for match in matches:
        addDir(match[2], match[1], 3, match[0]);
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

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
######################################### End of Generic Stuff ####################

def log(message):
    print "[ " + NAME +  "] " + message

def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
  
     
def GA(group,name):
    datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    VISITOR = os.path.join(datapath, 'visitor')
    if os.path.exists(VISITOR):
        VISITOR = open(VISITOR).read()
    else:
        if not os.path.isdir(datapath):
            try:
                os.makedirs(datapath)
            except IOError, e:
                print "Unable to create addon folder."
                return 

        from random import randint
        txtfile = open(VISITOR,"w") 
        txtfile.write(str(randint(0, 0x7fffffff)))
        txtfile.close()
        VISITOR = open(VISITOR).read()
    try:
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        VERSION = "4.2.8"
        UATRACK = "UA-38330258-1"
        PROPERTY_ID = environ.get("GA_PROPERTY_ID", UATRACK)
        PATH = "CanadaNepal"            
        utm_gif_location = "http://www.google-analytics.com/__utm.gif"
        if name=="None":
                utm_url = utm_gif_location + "?" + \
                        "utmwv=" + VERSION + \
                        "&utmn=" + str(randint(0, 0x7fffffff)) + \
                        "&utmp=" + quote(PATH) + \
                        "&utmac=" + PROPERTY_ID + \
                        "&utmcc=__utma=%s" % ".".join(["1", "1", VISITOR, "1", "1","2"])
        else:
            if group=="None":
                   utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH+"/"+name) + \
                            "&utmac=" + PROPERTY_ID + \
                            "&utmcc=__utma=%s" % ".".join(["1", "1", VISITOR, "1", "1","2"])
            else:
                   utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                            "&utmac=" + PROPERTY_ID + \
                            "&utmcc=__utma=%s" % ".".join(["1", "1", VISITOR, "1", "1","2"])
        if not group=="None":
                utm_track = utm_gif_location + "?" + \
                        "utmwv=" + VERSION + \
                        "&utmn=" + str(randint(0, 0x7fffffff)) + \
                        "&utmp=" + quote(PATH) + \
                        "&utmt=" + "events" + \
                        "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                        "&utmac=" + PROPERTY_ID + \
                        "&utmcc=__utma=%s" % ".".join(["1", "1", "1", VISITOR,"1","2"])

        print "Analitycs: %s" % utm_url
        send_request_to_google_analytics(utm_url)
        print "Analitycs: %s" % utm_track
        send_request_to_google_analytics(utm_track)
    except:
        print "================  CANNOT POST TO ANALYTICS  ================"
              
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
# 1: For latest videos
# 2: For indexing movies from HomePage
# 3: For getting a list of video links

if mode==None or url==None or len(url)<1:
    CATEGORIES()
elif mode==1:
    index(url)
elif mode==2:
    index_homepage(url)
elif mode==3:
    get_video_links(name, url)

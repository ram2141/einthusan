# CanadaNepal plugin written by humla.

import re
import os
import urlresolver
import urllib,urllib2
import xbmcplugin,xbmcgui
import xbmcaddon
from t0mm0.common.net import Net

# Taken from desitvforum xbmc plugin.
def GetDomain(url):
    print url
    tmp = re.compile('//(.+?)/').findall(url)
    domain = 'Unknown'
    if len(tmp) > 0:
        domain = tmp[0].replace('www.', '')
    return domain

def CATEGORIES():
    cwd = xbmcaddon.Addon().getAddonInfo('path')
    img_path = cwd + '/images/'
    addDir('Latest Videos', 'http://www.canadanepal.info', 1, 'http://canadanepal.info/images/tvprograms.gif')
    addDir('Live TV', cwd + '/resources/live_tv.xml', 6, 'http://canadanepal.info/images/banner/onlinetvf.jpg')
    addDir('Live Radio', 'http://canadanepal.info/fm/',4, 'http://canadanepal.info/images/listenfmlogo.gif')
    addDir('Daily News', 'http://canadanepal.info/dailynews/',7,'http://canadanepal.info/images/banner/samachar20.jpg')
    addDir('Sports News', 'http://canadanepal.info/sports/',8,'http://nepalitvshow.com/wp-content/uploads/2012/06/Scoreboard.jpg')
    addDir('Home Page', 'http://canadanepal.info',9,'http://a.webutation.net/3/3/canadanepal.net.jpg')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_sports(url, name):
    html = Net().http_GET(url).content
    name = re.compile("(Score.+?)<").findall(html)
    address = get_dailymotion_link(html)
    addDir(name[0], address[0],3,"")
    get_previous(url,name,"http://canadanepal.info/sports/update.php")

def get_previous(m_url, name, url):
    html = Net().http_GET(url).content

    match = re.compile('<a href="(.+?)" .+?>.+?>(.+?)<') .findall(html)
    for u,name in match:
        addDir(name, m_url+u, 2 ,"")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def get_news(url, name):
    html = Net().http_GET(url).content
    name=re.compile('Today\'s(.+?)<').findall(html)
    address = get_youtube_link(html)
    if (len(name) > 0):
        print name[0], address[0]
        addDir(name[0],address[0],3,"")
    get_previous(url, name, 'http://canadanepal.info/dailynews/update.php')

def SHOWRADIO(url):
    html = Net().http_GET(url).content
    match=re.compile('<li><a href="(.+?)"  class="normal"  target="_self" ><span>(.+?)</span>').findall(html)
    for fm_url,name in match:
            addDir(name,url + fm_url,5,"")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Scans the page to find streaming url for live radio.
def get_radio_links(html):
    match=re.compile('(.+?)file=(.+?)&amp').findall(html)
    if (len(match) == 0):
        match=re.compile('(.+?)stream1=(.+?)&amp;').findall(html)
    return [b for a,b in match]

# Scans the main FM page looking for stations that are available
def AUDIOLINKS(url, name):
    html = Net().http_GET(url).content
    match = get_radio_links(html)
    if (len(match) > 0):
        xbmc.Player().play(match[0], "")
    return 

# Removes html tags from NAME
def clear_htmltags(name):
    p = re.compile(r'<.*?>')
    result =  p.sub('', name)
    if (result[0] == '-'):
        result = result[1:]
    result = result.replace('&amp;', '').replace('&nbsp;','')
    return result

# Lists the new episodes of TV series
def INDEX(url):
    html = Net().http_GET(url).content
    match=re.compile('<div><font size="2">(.+?)<a href="(.+?)".+?Click').findall(html)
    image_base_url = xbmcaddon.Addon().getAddonInfo('path') + '/images/'
    for name,url in match:
        name = clear_htmltags(name)
        image_name = name[:4]
        image_url = image_base_url + image_name + '.jpg'
        #print image_url
        addDir(name,url,2,image_url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Show the list of live tv 
def SHOWLIVETVLIST(url):
    openfile = open(url, 'r')
    result = openfile.read()
    openfile.close()
    match = re.compile('<channel>((.|\n)+?)</channel>').findall(result)
    for info,_ in match:
        name = re.compile('<name>(.+?)</name').findall(info)
        picture = re.compile('<image>(.+?)</image>').findall(info)
        url = re.compile('<link>(.+?)</link>').findall(info)
        addLink(name[0], url[0],picture[0]) 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    return

def get_dailymotion_link(html):
    print "Scraping Dailymotion link"
    match=re.compile('"(http://www.dailymotion.com/video/.+?)"').findall(html)
    if (len(match) == 0):
        print "Dailymotion doing alternate scraping"
        match=re.compile('<iframe src="(.+?)"').findall(html)
    length = len(match)
    while length > 0:
        match[length-1] = match[length-1].replace('/embed','')
        length = length - 1
    return match

def get_youtube_link(html):
    print "Scraping youtube link"
    match=re.compile('"http://www.youtube.com/v/(.+?)"').findall(html)
    if (len(match) == 0):
        match = re.compile('"http://www.youtube.com/embed/(.+?)"').findall(html)
    match = set(match)  
    return ["http://www.youtube.com/watch?v="+a for a in match]

def get_blip_tv_link(html):
    print "Scraping blip tv link"
    match=re.compile('"(http://(www.)?blip.tv/play/.+?)"').findall(html)
    return [a for a,b in match]
    
def VIDEOLINKS(url,name):
    print "Getting video links"
    html = Net().http_GET(url).content
    match = get_youtube_link(html)
    if (len(match) == 0):
        match = get_blip_tv_link(html)
    if (len(match) == 0):
        match = get_dailymotion_link(html)
    i = 1
    length = len(match)
    image_path = xbmcaddon.Addon().getAddonInfo('path') + '/images/'
    all_url = ""
    for url in match:
        all_url = all_url + url + " "
        domain = GetDomain(url)
        addDir(domain + " : Part  " + str(i) + " of " + str(length), url, 3, image_path + domain + '.jpg')
        i = i + 1
    if (i > 2):
        addDir(domain + " : Play All", all_url, 3, image_path + domain + '.jpg');
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def play_video(url):
    log("Playing " + url)
    all_url = url.split()
    length = len(all_url)
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    for one_url in all_url:
        playlist.add(get_stream_url(one_url))
    player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    player.play(playlist)

def get_stream_url(url):
    domain = GetDomain(url)
    if domain == "blip.tv":
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        res=response.read()
        redirect =  response.geturl()
        response.close()
        v_id=re.compile('flash%2F(\d\d\d\d\d\d\d)').findall(redirect)
        stream_url= 'plugin://plugin.video.bliptv/?action=play_video&videoid=' + v_id[0]
    else:    
        stream_url = urlresolver.resolve(url)
    return stream_url
    
def get_homePageStuff(url):
    html = Net().http_GET(url).content
    data = re.compile('<div id="bodyimg">((.|\n)+?)<!-- Fm Programs -->((.|\n)+?)<div id="Interview With Raju Lama">((.|\n)+?)<div id="Calender">').findall(html)
    get_homePageStuffHelper(data[0][0])
    get_homePageStuffHelper(data[0][4])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_homePageStuffHelper(data):
    match = re.compile('.+?<a href="(.+?.html).+?".+?>(.+?)</a>(.+)').findall(data)
    length = len(match) - 1
    i = 0
    log(str(length))
    while (i < length):
        currentMatch = match[i]
        nextMatch = match[i+1]
        url = currentMatch[0]
        print currentMatch
        picture = get_Picture(currentMatch[1])
        if (url == nextMatch[0]):
            name = nextMatch[1]
            i = i + 1
        else:
            name = get_Name(currentMatch[2])
        i = i + 1
        if not(name == ""):
            addDir(clear_htmltags(name), url, 2, picture)
    if (i < length + 1):
        currentmatch = match[i]
        url = currentMatch[0]
        picture = get_Picture(currentMatch[1])
        name = get_Name(currentMatch[2])
        if not(name == ""):
            addDir(clear_htmltags(name), url, 2, picture)
        
def get_Picture(data):
    match=re.compile('<img.+?src="(.+?)"').findall(data)
    base_url = 'http://canadanepal.info/'

    if len(match) == 0 :
        return ""
    link = match[0]
    print link
    if (link.startswith("http") == False):
        link = base_url + link 
    return link

def get_Name(data):
    match=re.compile('<a href=.+?>(.+?)</a>').findall(data)    
    if (len(match) == 0):
        return ""
    return match[0]

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
    print "[CanadaNepal] " + message
              
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
# 2: Give the link of a page a serial (Meri Bassai 12th May) 
# 3: Play the video given the link
# 4: Give the list of available radio stations
# 5: Get link for each radio station
# 6: Chose live Tv from the main menu
# 7: Daily News scrapign for link
# 8: Look for sports in canadanepal.info/sports
# 9: Look for stuff in the homepage

if mode==None or url==None or len(url)<1:
        CATEGORIES()
elif mode==1:
        INDEX(url)
elif mode==4:
        SHOWRADIO(url)
elif mode==6:
        SHOWLIVETVLIST(url)
elif mode==2:
        VIDEOLINKS(url,name)
elif mode==5:
        AUDIOLINKS(url,name)
elif mode==3:
        play_video(url) 
elif mode==7:
        get_news(url, name)
elif mode==8:
        get_sports(url, name)
elif mode==9:
        get_homePageStuff(url)

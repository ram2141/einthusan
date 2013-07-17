# Ustv.cc plugin written by humla.

import os
import re
import urllib, urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
from t0mm0.common.net import Net
from metahandler import metahandlers

ADDON = xbmcaddon.Addon(id='plugin.video.ustvcc')

def get_net():
  user_agent = "Mozilla/5.0 (X11; U; GNU Hurd; C -) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.10.1"
  return Net(user_agent=user_agent)

def http_get(url):
  net = get_net()
  try:
      return net.http_GET(url).content.encode("utf-8")
  except urllib2.URLError, e:
      xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to connect to website', '', '') 
      return ""

def http_post(url, post_data):
  net = get_net()
  try:
      return net.http_POST(url, post_data).content.encode("utf-8")
  except urllib2.URLError, e:
      xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to connect to website', '', '') 
      return ""  

## Not used..
def create_cookie_file():
  ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
  cookie_file = os.path.join(ADDON_USERDATA_FOLDER, 'cookies')
  print cookie_file
  if not os.path.exists(ADDON_USERDATA_FOLDER):
      print "Creating addon directory in userdata/addon_data"
      os.makedirs(ADDON_USERDATA_FOLDER)
  if not os.path.exists(cookie_file):
      print "Creating the cookie file"
      open(cookie_file,'w').close()
  return cookie_file

##
# Prints the main categories. Called when id is 0.
##
def main_categories(name, url, db_id, series_name, season):
  cwd = ADDON.getAddonInfo('path')
  img_path = cwd + '/images/' 

  url = 'http://www.ustv.cc/episode/'

  addDir('A-Z', url, 3, '')
  addDir('Hot TV Series', '', 7, '')
  addDir('Latest Updates TV Series', '', 8, '')
  addDir('New TV Episodes', '', 8, '')
  #addDir('Favourites', '', 8, '')
  #addDir('Search', '', 6, '')
  addDir('Settings', '', 9, '') 
  xbmcplugin.endOfDirectory(int(sys.argv[1]))

## Context menu
#listitem.addContextMenuItems(cm, replaceItems=True)
#  runstring = 'RunPlugin(%s)' % addon.build_plugin_url({'mode':'SaveFav', 'section':section, 'title':title, 'url':BASE_URL+resurl, 'year':year})
#           cm.append(('Add to Favorites', runstring,))
##

def a_z_view(name, url, db_id, series_name, season):
  azlist = map (chr, range(97,122))

  addDir('Numerical', url + 'num.htm', 5, '')

  for letter in azlist:
      addDir(letter, url + letter + '.htm', 5, '', db_id=db_id)
  xbmcplugin.endOfDirectory(int(sys.argv[1]))   

def list_hot_TV_series (name, url, db_id, series_name, season):
  progressBar = xbmcgui.DialogProgress()
  progressBar.create(ADDON.getAddonInfo('name'), "Getting metadata")
  progressBarValue = 0

  url = 'http://ustv.cc/episode/watch-Arrow-online.htm'
  html = http_get(url)
  matches = re.compile('<span class="jumu"><a title=".+?" href="(/episode/.+?.htm)">(.+?)</a></span><span class="nabe">(.+?)</span>').findall(html)

  progressBarValue = 10
  progressBar.update(progressBarValue)

  BASE_URL = "http://ustv.cc"
  metahandle = metahandlers.MetaData()

  if (len (matches) > 0):
    interval = 90 / len(matches)
  
  for link, name, clicks in matches:
      displayName = name + " : [COLOR red]" + clicks + " clicks [/COLOR]"
      add_tv_show_in_list(metahandle, BASE_URL + link, name, displayName)
      progressBarValue = progressBarValue + interval
      progressBar.update(progressBarValue)

  xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
  xbmc.executebuiltin("Container.SetViewMode(503)")  
  xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_meta_tv_show(metahandle, name):
  return metahandle.get_meta('tvshow', name)

def add_tv_show_in_list(metahandle, link, name, displayName):
  meta = get_meta_tv_show(metahandle, name) 
  cover = meta['banner_url']
  addDir(name, link, 1, cover, meta=meta, db_id=meta['imdb_id'], displayName=displayName, series_name=name)
  return

##
# Shows a list of Tv series. Called when mode is 5.
##
def list_tv_series_list(name, url, db_id, series_name, season):
  html = http_get(url)
  list_tv_series_list_aux(html)

def list_tv_series_list_aux(html):
  progressBar = xbmcgui.DialogProgress()
  progressBar.create(ADDON.getAddonInfo('name'), "Getting metadata")
  progressBarValue = 0

  bulk = re.compile('<dl class="list_wut">((.|\n)+?)</dl>').findall(html)

  progressBarValue = 7
  progressBar.update(progressBarValue)

  if (len(bulk) > 0):
    metahandle = metahandlers.MetaData()
    matches = re.compile('title=".+?" href="(/episode/.+?.htm)">(.+?)</a>').findall(bulk[len(bulk) - 1][0])
    BASE_URL = "http://ustv.cc"

    progressBarValue = 15
    progressBar.update(progressBarValue)

    if (len(matches) > 0):
      interval = 85 / len(matches) 

    for link, name in matches:
      add_tv_show_in_list(metahandle, BASE_URL + link, name, '')
      progressBarValue = progressBarValue + interval
      progressBar.update(progressBarValue)

    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    xbmc.executebuiltin("Container.SetViewMode(503)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))    
  else:
    # Display a dialog
    xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Cant get any TV Series', '', '') 

#
# List the seasons for a specific TV series. Called when mode is 1.
#
def list_seasons(name, url, db_id, series_name, season):
  html = http_get(url)

  progressBar = xbmcgui.DialogProgress()
  progressBar.create(ADDON.getAddonInfo('name'), "Getting metadata")
  progressBarValue = 0

  matches = re.compile(' <label  id=".+?".+?onclick="selecttab\(\'(.+?)\'\)" ').findall(html)

  metahandler = metahandlers.MetaData()
  seasons_data = metahandler.get_seasons(name, db_id, matches, overlay=6)

  progressBarValue = 10
  progressBar.update(10)

  if (len(matches) > 0):
    interval = 90 / len(matches)

  i = 0
  for season in matches:
      season_data = seasons_data[i]
      cover = season_data['cover_url']
      addDir(season, url, 4, cover, "Season " + season, meta=season_data, db_id=db_id, season=season, series_name=series_name)  
      i = i + 1
      progressBarValue = progressBarValue + interval
      progressBar.update(progressBarValue)

  xbmcplugin.endOfDirectory(int(sys.argv[1]))    

# Lists all the episdoes in the given season.
# Called when mode is 4
#
def list_episodes_in_season(name, url, db_id, series_name, season):
  progressBar = xbmcgui.DialogProgress()
  progressBar.create(ADDON.getAddonInfo('name'), "Getting metadata")
  progressBarValue = 0

  tab = "stab" + name
  html = http_get(url)
  compile_string = '<ul class="ju_list" id="' + tab + '"((.|\\n)+?)</ul>'
  bulk = re.compile(compile_string).findall(html)

  progressBarValue = 10
  progressBar.update(progressBarValue)

  if (len(bulk) > 0):
      name_matches = re.compile('<li>(.+?)\n').findall(bulk[0][0])
      links_matches = re.compile('<a title=".+?" href="(.+?)"').findall(bulk[0][0])
      name_links_matches = zip(name_matches, links_matches)

      BASE_URL = "http://www.ustv.cc"
      metahandle = metahandlers.MetaData()
      progressBarValue = 20
      progressBar.update(progressBarValue)

      if (len(name_matches) > 0):
        interval = 80 / len (name_matches)

      for e_name, link in name_links_matches:
          ep_number = int(e_name.split(' ')[0])
          meta = metahandle.get_episode_meta('', db_id, name, ep_number)
          addDir(e_name, BASE_URL + link, 2, meta['cover_url'], db_id=db_id, meta=meta, season=season, series_name=series_name)
          progressBarValue = progressBarValue + interval
          progressBar.update(progressBarValue)
      xbmcplugin.endOfDirectory(int(sys.argv[1]))    
  else:
      xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Cant find any episodes', '', '') 

# Displays the list of new tv series.
# Called when mode is 8
def list_latest_update_tv_series(name, url, db_id, series_name, season):
  BASE_URL = "http://ustv.cc"
  html = http_get(BASE_URL)

  bulk = re.compile('<div class="hot_aes">' + name + '</div>((.|\n)+?)</ul>').findall(html)

  if (len(bulk) > 0):
    progressBar = xbmcgui.DialogProgress()
    progressBar.create(ADDON.getAddonInfo('name'), "Getting metadata")
    progressBarValue = 0;

    metahandle = metahandlers.MetaData()
    matches = re.compile('<a title=".+? " href="(/episode/(.+?).htm)">(.+?)</a>.+?color="#FF0000">(.+?)</font>').findall(bulk[0][0])

    progressBar.update(10)
    progressBarValue = 10;

    if (len(matches) > 0):
      interval = 90 / len(matches) 

    for link, base_name, name, ep in matches:
        ep = ep.replace('&nbsp;','')
        displayName = name + ":[COLOR red]" + ep +"[/COLOR]"
        add_tv_show_in_list(metahandle, BASE_URL + link, name, displayName)
        progressBarValue =  progressBarValue + interval
        progressBar.update(progressBarValue)
    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    xbmc.executebuiltin("Container.SetViewMode(503)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))    
  else:
    xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Cannot find TV series', '', '') 

##
# Shows the search box for serching. Shown when the id is 6.
##
def show_search_box(name, url, db_id, series_name, season):
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
def play_video(name, url, db_id, series_name, season):
  login_url = "http://ustv.cc/login.php"
  params = {}
  params['username'] = 'hello_how'
  params['password'] = 'hello_how'
  params['joinus'] = '1'
  params['submit'] = ' Sign in '
  http_post(login_url, params)

  html =  http_get(url)
  match = re.compile('[\'\"].+?\?key=(.+?)[\"\']').findall(html)


  if (len (match) > 0):
      
      key = 'http://d.ustv.cc/ip.mp4?key=' + urllib.quote(match[0])
      playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
      playlist.clear()
      listitem = xbmcgui.ListItem(name)
      playlist.add(key, listitem)
      xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)

      ## Call metahandler and set viewed to true
      ep_number = int(name.split(' ')[0])
      metahandle = metahandlers.MetaData()
      metahandle.change_watched(media_type='episode', name=name, imdb_id=db_id, season=season, episode=ep_number, watched=7)
  else:
      xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Cannot find a video stream', '', '') 

##
# Displays the setting view. Called when mode is 12
##
def display_setting(name, url, db_id, series_name, season):
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


def addDir(name, url, mode, iconimage, displayName='', meta = {}, db_id='', series_name='', season=''):
  if (displayName == ''):
    displayName = name
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&dbid="+urllib.quote_plus(db_id)+"&season="+urllib.quote_plus(season)+"&sn="+urllib.quote_plus(series_name)
  liz=xbmcgui.ListItem(displayName, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  meta["Title"] = displayName
  liz.setInfo( type="Video", infoLabels=meta )
  liz.setProperty('IsPlayable', 'true')
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
  return ok

params=get_params()
url=None
name=None
mode=0
db_id=''
series_name=''
season=''

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
  db_id=urllib.unquote_plus(params["dbid"])
except:
  pass

try:
  season=urllib.unquote_plus(params["season"])
except:
  pass

try:
  series_name=urllib.unquote_plus(params["sn"])
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
function_map[9] = display_setting



function_map[mode](name, url, db_id, series_name, season)
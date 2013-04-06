import os
import urllib2
import xbmcplugin
import xbmcaddon

from t0mm0.common.net import Net

def http_get(url, username='', password =''):
    net = Net()
    if (username != '' and password != ''):
        form_data = {}
        form_data['username'] = username
        form_data['password'] = password
        login_url = "http://www.einthusan.com/etc/login.php"
        http_post(login_url, form_data)
    try:
        return net.http_GET(url).content
    except urllib2.URLError, e:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to connect to website', '', '') 
        return ""

def http_post(url, postData):
    try:
        return Net().http_POST(url, postData).content
    except urllib2.URLError, e:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to login to website', '', '') 
        return ""
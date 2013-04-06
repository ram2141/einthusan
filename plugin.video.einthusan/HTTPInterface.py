import os
import urllib2

def http_get(url, username='', password =''):
    if (username != '' and password != ''):
        form_data = {}
        form_data['username'] = username
        form_data['password'] = password
        login_url = "http://www.einthusan.com/etc/login.php"
        http_post(login_url, form_data)
    try:
        return urllib2.urlopen(url).read() 
    except urllib2.URLError, e:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to connect to website', '', '') 
        return ""

def http_post(url, postData):
    try:
        return urllib2.urlopen(url, postData).read()
    except urllib2.URLError, e:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to login to website', '', '') 
        return ""
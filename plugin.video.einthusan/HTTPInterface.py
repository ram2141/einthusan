import os
import urllib, urllib2

def http_get(url, username='', password =''):
    if (username != '' and password != ''):
        form_data = {}
        form_data['username'] = username
        form_data['password'] = password
        login_url = "http://www.einthusan.com/etc/login.php"
        http_post(login_url, postData=form_data)
    try:
        return urllib2.urlopen(url).read() 
    except urllib2.URLError, e:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to connect to website', '', '') 
        return ""

def http_post(url, postData={}, data=''):
    try:
        if (data == ''):
            data = urllib.urlencode(postData)
        return urllib2.urlopen(url, data).read()
    except urllib2.URLError, e:
        xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), 'Unable to login to website', '', '') 
        return ""

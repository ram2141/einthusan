import os
import urllib, urllib2
import urlparse

from t0mm0.common.net import Net

def http_get(url, username='', password =''):
    if (username != '' and password != ''):
        form_data = {}
        form_data['username'] = username
        form_data['password'] = password
        login_url = "http://www.einthusan.com/etc/login.php"
        http_post(login_url, postData=form_data)
    try:
        return Net().http_GET(url).content
    except urllib2.URLError, e:
        return ""

def http_post(url, postData={}, data=''):
    try:
        if (data != ''):
            postData = dict(urlparse.parse_qsl(data))
        return Net().http_POST(url, postData).content
    except urllib2.URLError, e:
        return ""

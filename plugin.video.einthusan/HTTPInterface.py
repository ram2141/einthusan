import os
import urllib, urllib2
import urlparse

import requests

headers = {'User-Agent':'AppleCoreMedia/1.0.0.12B411 (iPhone; U; CPU OS 8_1 like Mac OS X; en_gb)'}

def http_get(url, headers=None, cook=None):
    try:
        r = requests.get(url, headers=headers, cookies=cook).content
        return r
    except urllib2.URLError, e:
        return ''

def http_post(url, cookie_file='', postData={}, data=''):
    try:
        if (data != ''):
            postData = dict(urlparse.parse_qsl(data))
        net = Net(cookie_file=cookie_file)
        return net.http_POST(url,postData).content
    except urllib2.URLError, e:
        return ''

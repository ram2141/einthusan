import os
import urllib, urllib2
import urlparse
import zlib 

headers = {'Referer':'http://www.einthusan.com/',
           'Origin':'http://www.einthusan.com/',
           'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-gb) AppleWebKit/525.1+ (KHTML, like Gecko, Safari/525.1+) midori/1.19'}

def http_get(url, cookie_file='',username='', password =''):
    if (username != '' and password != ''):
        form_data = {}
        #form_data['username'] = username
        #form_data['password'] = password
        #login_url = 'http://www.einthusan.com/etc/login.php'
        #http_post(login_url, postData=form_data)
    try:
        #req = urllib2.Request(url, '', headers)
        gzipContent = urllib2.urlopen(url).read()
        return  zlib.decompress(gzipContent, 16+zlib.MAX_WBITS)
    except urllib2.URLError, e:
        print e 
        print "Error when sending a http get request to " + url 
        return ''

def http_post(url, cookie_file='', postData={}, data=''):
    try:
        if (data != ''):
            postData = dict(urlparse.parse_qsl(data))
        #net = Net(cookie_file=cookie_file)
        #return net.http_POST(url,postData).content
        postMsg=urllib.urlencode(postData)
        req = urllib2.Request(url, postMsg, headers)
        return urllib2.urlopen(req).read()
    except urllib2.URLError, e:
        print "Error when sending a http post request to " + url 
        return ''

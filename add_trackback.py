data = {
    'title':"My Blog Post",
    'excerpt':'the beggining of the content of my blog post',
    'url':'http://linuxfr.org',
    'blog_name':'The name of my blog'
}

import urllib
import httplib
httplib.HTTPConnection.debuglevel = 1
params = urllib.urlencode(data)
print params
f = urllib.urlopen("http://127.0.0.1:8000/2008/04/07/item-1-2/trackback/", params)
print f.read()
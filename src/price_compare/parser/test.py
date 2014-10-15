#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
import urllib2

req = urllib2.Request('http://s.taobao.com/search?q=ipad')
response = urllib2.urlopen(req)

print response.read()
"""


import urllib2

from GetItems import *
import json

g = Item_Spider(u"iphone5")
json_taobao = g.get_item_jd()

print json_taobao

"""
new = json.loads(json_taobao)
print new
print type(new)
"""

"""
import urllib2
req = urllib2.Request('http://search.jd.com/Search?enc=utf-8&keyword=ipad')
req2 = urllib2.Request('http://search.jd.com/Search?keyword=ipad&enc=utf-8&area=15')
response = urllib2.urlopen(req)
print "Open Done"
#All page to feed must be converted to unicode first!
page = response.read()

print page
"""
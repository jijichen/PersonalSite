# -*- coding: utf-8 -*-

import urllib2
import urllib
from HTMLParser import HTMLParser
import re

import json

#Flags
DEBUG = True

""" For item data info and items list """
class ItemInfo():
	def __init__(self):
		self.summary   = ''
		self.item_id   = ''
		self.pic_src   = ''
		self.item_href = ''
		self.price     = -1
		self.shipping  = -1
		self.num_att   = 6

# create a subclass and override the handler methods
"""
Paser for a html page from Taobao.com

<div col item icon-datalink>					0
 <div item-box>									1
  <div pic> ---> <img src=>						2	
  <h3 summary> ---> <a title=>					2
			   ---> <a href=>
   <div col price> -->data 						3
   <div col end shipping> --> data(rm space)	3

"""
class HTMLParser_taobao(HTMLParser):

	__item_class = 'col item icon-datalink'

	def __init__(self):
		HTMLParser.__init__(self)
		self.__tag_level = 0
		self.__pic_sum_level = 2
		self.__pri_shi_level = 3

		self.__in_item = False
		self.__in_item_pic = False
		self.__in_item_summary = False
		self.__in_item_price = False
		self.__in_item_shipping = False
		self.info = ItemInfo()
		self.items_dic_array = []

	def __extract_int(self,data):
		#print type(data.decode('gbk'))
		#print data.decode('gbk')
		pat = re.compile(ur'[0-9]+')
		res = pat.search(data.encode('gbk'))
		if res:
			return int(res.group())
		return -1

	def __obj2dic(self,obj):
		_dict = {}

		memberlist = [m for m in dir(obj)]			
		for m in memberlist:
			if m[0] != '_' and not callable(m):
				#print obj.item_id
				_dict[m] = getattr(obj,m)

		#print _dict
		return _dict
		
	def handle_starttag(self, tag, attrs):
		nid = ''
		#Find the outmost div block for item and get item id
		if self.__in_item == False:
			if (tag == 'div'):
				for attPair in attrs:
					if (attPair[0] == 'class' and attPair[1] == self.__item_class):
						self.__tag_level = 0
						self.__in_item = True
						self.info.item_id = nid

					if (attPair[0] == 'nid'):
						nid = attPair[1]
						if (self.__in_item == True) : self.info.item_id = nid

		#Otherwise it's in the block, look for pic(in div) and summary(h3)
		elif (self.__in_item == True and (tag == 'div' or tag == 'h3')):
			#Inc the current level in an item
			self.__tag_level = self.__tag_level+1 
			#For pics and summary
			if (self.__tag_level == self.__pic_sum_level):
				for attPair in attrs:					
					if (attPair[0] == 'class' and attPair[1] == 'pic') : self.__in_item_pic = True
					if (attPair[0] == 'class' and attPair[1] == 'summary') : self.__in_item_summary = True
			#For price and shipping
			if (self.__tag_level == self.__pri_shi_level):
				for attPair in attrs:
					if (attPair[0] == 'class' and attPair[1] == 'col price') : self.__in_item_price = True					
					if (attPair[0] == 'class' and attPair[1] == 'col end shipping') : self.__in_item_shipping = True
			
		#Get item image
		elif (self.__in_item == True and self.__in_item_pic == True and tag == 'img'):
			for attPair in attrs:
				if (attPair[0] == 'src') : self.info.pic_src = attPair[1]

		#Get summary and href
		elif (self.__in_item == True and self.__in_item_summary == True and tag == 'a'):
			for attPair in attrs:
				if (attPair[0] == 'title') : self.info.summary = attPair[1]
				if (attPair[0] == 'href') : self.info.item_href = attPair[1]

	def handle_endtag(self, tag):
		if (self.__in_item == True and (tag == 'div' or tag == 'h3')):
			#At the outmost level for an Item
			if (self.__tag_level == 0):
				self.__in_item = False

				one_item_dict = self.__obj2dic(self.info)
				self.items_dic_array.append(one_item_dict)
				print self.items_dic_array
				#self.items.add_item(self.info)

				if DEBUG == True:
					print '----------'
					print 'id:' + self.info.item_id.encode('utf-8')
					print 'summary:' + self.info.summary.encode('utf-8')
					print 'pic_src:' + self.info.pic_src
					print 'test:' + str(self.__extract_int('none'))
					print 'shipping:' + str(self.info.shipping)
					print 'Price:' + str(self.info.price)
					print 'href:' + self.info.item_href

			elif (self.__tag_level > 0):
				if (self.__tag_level == 3):
					if (self.__in_item_price == True) : self.__in_item_price = False
					if (self.__in_item_shipping == True) : self.__in_item_shipping = False
				if (self.__tag_level == 2):
					if (self.__in_item_pic == True) : self.__in_item_pic = False
					if (self.__in_item_summary == True) : self.__in_item_summary = False

				self.__tag_level -= 1

			else : print "Paser Wrong tag no pare" #!TODO: add an exception

	def handle_data(self, data):
		if (self.__in_item == True):
			if (self.__in_item_price == True) : self.info.price = self.__extract_int(data)
			if (self.__in_item_shipping == True) : self.info.shipping = self.__extract_int(data)		

	def get_items_dic_list(self):
		return self.items_dic_array

"""
Paer for type2 items from Taobao.com (Those items that is specific by Taobao)
Which leads to a new page view by taobao and the parser needs to be reconstructed.

Struct:
<div row item icon-datalink>				0
	<div col pic>								1
		...<img src=>
	<div col title>
		...<a title=>
		...<a href=>
	<div col total>
		...<div class="price"> --> data
		...<div class="shipping"> -> data
"""
class HTMLParser_taobao2(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.att_count = 0

		self.__item_class  = 'row item icon-datalink'
		self.__pic_class   = 'col pic'
		self.__title_class = 'col title'
		self.__total_class = 'col total'

		self.__in_item         = False
		self.__in_item_pic     = False
		self.__in_item_pic_210 = False
		self.__in_item_price   = False
		self.__in_item_title   = False

		self.info  = ItemInfo()
		self.items_dic_array = []

	def __extract_int(self,data):
		#print type(data.decode('gbk'))
		#print data.decode('gbk')
		pat = re.compile(ur'[0-9]+')
		res = pat.search(data.encode('gbk'))
		if res:
			return int(res.group())
		return -1

	def __obj2dic(self,obj):
		_dict = {}

		memberlist = [m for m in dir(obj)]			
		for m in memberlist:
			if m[0] != '_' and not callable(m):
				#print obj.item_id
				_dict[m] = getattr(obj,m)

		#print _dict
		return _dict

	def handle_starttag(self, tag, attrs):
		nid = ''

		#Find the outmost div block for item and get item id	
		if (self.__in_item == False):
			if (tag == 'div'):
				for attPair in attrs:
					if (attPair[0] == 'class' and attPair[1] == self.__item_class):					
						self.__in_item          = True			
						self.att_count          = 0
						self.__in_item_pic      = False
						self.__in_item_total    = False
						self.__in_item_price    = False
						self.__in_item_shipping = False
						self.__in_item_title    = False
						self.info               = ItemInfo()

						if (nid) and (not self.info.item_id):
							self.info.item_id = nid
							self.att_count += 1

					if (attPair[0] == 'nid'):
						nid = attPair[1]
						if (self.__in_item == True) : 
							self.info.item_id = nid
							self.att_count += 1

		#Otherwise it's in the block, look for pic title price
		#Start use tag count for div 
		elif (self.__in_item == True and tag == 'div'):
			for attPair in attrs:
				if attPair[0] == 'class':
				 	if attPair[1]   == self.__pic_class:
						self.__in_item_pic   = True
						self.__in_item_total = False
						self.__in_item_title = False
					elif attPair[1] == self.__total_class:
						self.__in_item_pic   = False
						self.__in_item_total = True
						self.__in_item_title = False
					elif attPair[1] == self.__title_class:
						self.__in_item_pic   = False
						self.__in_item_total = False
						self.__in_item_title = True
					elif attPair[1] == self.__item_class:
						#Idealy this condition should not happen
						#But if it happend, just discard current item and try for next one
						self.__in_item       = False
						self.att_count	 	 = 0
						self.__in_item_pic   = False
						self.__in_item_total = False
						self.__in_item_title = False
						self.info 			 = ItemInfo()
						print "Error: att_count:" + str(self.att_count)
					#---------------------------------------------------------
					elif self.__in_item_total and attPair[1] == 'price':
						self.__in_item_price = True
					elif self.__in_item_total and attPair[1] == 'shipping':
						self.__in_item_shipping = True
		#In specific block for attribute						
		elif (self.__in_item == True):
			print self.att_count
			in_title = False
			in_href  = False

			if (self.__in_item_title == True and tag == 'a'):
				for attPair in attrs:
					if attPair[0] == 'trace' and attPair[1] == 'auction':
						in_title = True
						in_href  = True

					if attPair[0] == 'title' and in_title:
						self.info.summary   = attPair[1]
						print "title"
						self.att_count += 1
						in_title = False

					if attPair[0] == 'href' and in_href:
						self.info.item_href = attPair[1]
						print "href"
						self.att_count += 1
						in_href = False

			if (self.__in_item_pic == True and tag == 'a'):
				for attPair in attrs:
					if attPair[0] == 'class' and attPair[1] == 's210':
						self.__in_item_pic_210 = True

			if (self.__in_item_pic == True and tag == 'img'):
				for attPair in attrs:
					if attPair[0] == 'src' and self.__in_item_pic_210:
						self.info.pic_src = attPair[1]
						print "pic_src"
						self.att_count += 1
						self.__in_item_pic_210 = False

	def handle_endtag(self, tag):
		if (self.__in_item == True and self.att_count == self.info.num_att):
			#self.items.add_item(self.info)
			#print "Add one item"
			one_item_dict = self.__obj2dic(self.info)
			print one_item_dict
			self.items_dic_array.append(one_item_dict)
			print self.items_dic_array
			self.__in_item = False

	def handle_data(self, data):
		if (self.__in_item == True):
			if (self.__in_item_price == True) : 
				self.info.price      = self.__extract_int(data)
				print "Price"
				self.att_count += 1
				self.__in_item_price = False
			if (self.__in_item_shipping == True) : 
				self.info.shipping      = self.__extract_int(data)	
				print "shipping"
				self.att_count += 1	
				self.__in_item_shipping = False

	def get_items_dic_list(self):
		#print self.items_dic_array
		return self.items_dic_array

"""
Parser for amazon.cn.

Struct:
<div result (firstResultRow) product>
	<div productImage>
		<a href=item_href>
			<img src=pic_src>
	<div productTitle>
		<a>summary
	<div newPrice>
		<span>


"""
class HTMLParser_amazon(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.att_count = 0
		self.items_dic_array = []
		
		self.__item_class  = 'result product'
		self.__item_class2 = 'result firstResultRow product'
		
		self.__in_item         = False
		self.__in_item_pic     = False
		self.__in_item_title   = False
		self.__in_item_price   = False
		self.__in_item_price_n = False
		self.__in_item_summary = False

	def __extract_int(self,data):
		#print type(data.decode('gbk'))
		#print data.decode('gbk')
		pat = re.compile(ur'[0-9]+')
		res = pat.search(data.encode('utf-8'))
		if res:
			return int(res.group())
		return -1

	def __obj2dic(self,obj):
		_dict = {}

		memberlist = [m for m in dir(obj)]			
		for m in memberlist:
			if m[0] != '_' and not callable(m):
				#print obj.item_id
				_dict[m] = getattr(obj,m)

		#print _dict
		return _dict

	def handle_starttag(self,tag,attrs):

		if self.__in_item == False:
			if (tag == 'div'):
				for attPair in attrs:
					if (attPair[0] == 'class') and ( self.__item_class in attPair[1] or self.__item_class2 in attPair[1] ):
						self.att_count         = 0         
						self.__in_item_pic     = False     
						self.__in_item_price   = False     
						self.__in_item_title   = False     
						self.__in_item_summary = False   
						self.__in_item_price_n = False   
						self.info              = ItemInfo()
						self.info.num_att      = 4         
						self.__in_item         = True      
		elif self.__in_item == True:
			if (tag == 'div'):
				for attPair in attrs:
					if (attPair[0] == 'class'):
						if (attPair[1] == 'productImage'):
							#print "in productImage"
							self.__in_item_pic   = True
							self.__in_item_price = False
							self.__in_item_title = False
						if (attPair[1] == 'productTitle'):
							self.__in_item_pic   = False
							self.__in_item_price = False
							self.__in_item_title = True
						if (attPair[1] == 'newPrice'):
							self.__in_item_pic   = False
							self.__in_item_price = True
							self.__in_item_title = False
			elif (tag == 'a'):
				if self.__in_item_pic:
					for attPair in attrs:
						if (attPair[0] == 'href'):
							self.info.item_href = attPair[1]
							self.att_count += 1
							#print "href"
				if self.__in_item_title:
					self.__in_item_summary = True
			elif (tag == 'img'):
				if self.__in_item_pic:
					for attPair in attrs:
						if (attPair[0] == 'src'):
							self.info.pic_src = attPair[1]
							self.att_count += 1
							#print "img"
			elif (tag == 'span'):
				if self.__in_item_price:
					self.__in_item_price_n = True

	def handle_data(self, data):
		if (self.__in_item == True):
			if (self.__in_item_price_n):
				self.info.price = self.__extract_int(data)
				print data.encode("utf-8")
				self.att_count += 1
				self.__in_item_price_n = False

			if (self.__in_item_summary):
				self.info.summary = data
				self.att_count += 1
				self.__in_item_summary = False
				#print self.i

	def handle_endtag(self,tag):
		if (self.__in_item == True):
			if (self.att_count == self.info.num_att):
				#print "Get one item"
				one_item_dict = self.__obj2dic(self.info)
				#print one_item_dict
				self.items_dic_array.append(one_item_dict)
				#print self.items_dic_array
				self.__in_item = False

	def get_items_dic_list(self):
		return self.items_dic_array

#Common interface provided to user
class Item_Spider():
	def __init__(self,kw):	
		if not isinstance(kw,unicode):
			#TODO:raise exception
			pass			
		self.kword = kw.encode('gb2312')
		self.dict = {'q':self.kword,}
		self.url_str = urllib.urlencode(self.dict)
		#print self.url_str

	def __paser_taobao(self):
		p = HTMLParser_taobao()
		p.feed(self.page_u)
		list_site = p.get_items_dic_list()

		if list_site:
			return list_site
		else:
			#print "In parser 2"
			p2 = HTMLParser_taobao2()
			p2.feed(self.page_u)
			list_site = p2.get_items_dic_list()
			return list_site

	def __parser_amazon(self):
		p = HTMLParser_amazon()
		p.feed(self.page_u)
		list_site = p.get_items_dic_list()

		return list_site

	def __parser_jd(self):
		p = HTMLParser_jd()
		p.feed(self.page_u)
		list_site = p.get_items_dic_list()


	def get_item_taobao(self):
		req = urllib2.Request('http://s.taobao.com/search?q=' + self.kword)
		response = urllib2.urlopen(req)

		#All page to feed must be converted to unicode first!
		self.page = response.read()
		self.page_u = self.page.decode('gbk')
		
		#print "The page is Unicode ?",
		list_site = self.__paser_taobao()
		#print list_site

		for item in list_site:
			for k in item:
				if k == 'pic_src':
					print item[k]
				
		return json.dumps(list_site)

	def get_item_amazon(self):
		req = urllib2.Request('http://www.amazon.cn/s?&field-keywords=' + self.kword)
		response = urllib2.urlopen(req)

		#All page to feed must be converted to unicode first!
		self.page = response.read()
		self.page_u = self.page.decode('utf-8')

		list_site = self.__parser_amazon()

		return json.dumps(list_site)

	def get_item_jd(self):
		req = urllib2.Request('http://search.jd.com/Search?enc=utf-8&keyword=' + self.kword.encode("utf-8"))
		req.add_header('User-agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)')
		response = urllib2.urlopen(req)

		#All page to feed must be converted to unicode first!
		self.page = response.read()

		self.page_u = self.page.decode('gb2312')

		list_site = self.__parser_jd()
		return self.page_u



	

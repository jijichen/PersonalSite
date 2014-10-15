# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

#shortcuts
from django.shortcuts import get_object_or_404,get_list_or_404,render

from price_compare.parser import GetItems
import json

def index(request):
	items = []
	if request.method == 'POST':
		item_name = request.POST['item_name']
		item_name_u = item_name.encode('utf-8')

		spider = GetItems.Item_Spider(item_name_u)
		items_json_taobao = spider.get_item_taobao()
		items_json_amazon = spider.get_item_amazon()

		item_array = json.loads(items_json_taobao)	
		ind = 0
		rows_taobao = []
		row = []
		for item in item_array:
			row.append(item)
			ind += 1
			if (ind % 4 == 0):
				rows_taobao.append(row)
				row = []
				ind = 0

		item_array = json.loads(items_json_amazon)
		ind = 0
		rows_amazon = []
		row = []
		for item in item_array:
			row.append(item)
			ind += 1
			if (ind % 4 == 0):
				rows_amazon.append(row)
				row = []
				ind = 0

		return render(request,'compare_list.html',{'items_taobao':rows_taobao,'items_amazon':rows_amazon})
	else:
		return render(request,'compare_list.html',{'items':[]})
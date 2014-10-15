# Create your views here.
from django.template import loader,Context
from django.db import models
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import BlogPost,BlogCategory

from django.core.urlresolvers import reverse

#shortcuts
from django.shortcuts import get_object_or_404,get_list_or_404,render

#forms
from blog.forms import CommentForm

g_cates = {}
g_year_list = []


def blog_list(request,blog_year=0,blog_month=0,blog_cate=''):
	#filter, there should not be any spaces before and after '='
	posts = BlogPost.objects.filter(private__exact=False).order_by('timestamp')
	cates = BlogCategory.objects.all()
	covers = []

	year_cont = []
	month_dic = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
				 7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
	
	month_dic_reverse = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
				 "July":7,"August":8,"September":9,"October":10,"November":11,"December":12}

	for post in posts:
		#post.body = post.generate_summary()
		
		b_inserted = False
		for dicts in year_cont:
			if dicts["year"] == post.timestamp.year:
				dicts[month_dic[post.timestamp.month]] += 1
				b_inserted = True
		if (not b_inserted):
			temp_dic = {}
			for i in range(1,12):
				temp_dic[month_dic[i]] = 0 
			temp_dic[month_dic[post.timestamp.month]] = 1
			temp_dic["year"] = post.timestamp.year
			year_cont.append(temp_dic)

	posts = posts.order_by('-timestamp','category__cate')

	if (blog_year != 0):
		posts = posts.filter(timestamp__year=blog_year)
		
	if (blog_month != 0):
		posts = posts.filter(timestamp__month=blog_month)

	if (blog_cate != ''):
		posts = posts.filter(category__cate=blog_cate)
	
	for post in posts:
		cover_src = post.get_cover()
		if (cover_src):
			post.cover_src = cover_src

	return render(request,'blog_list.html',{'posts':posts,'cates':cates,'year_list':year_cont,'mon_dic_rev':month_dic_reverse}) 

#Test view for blog content
def blog_detail(request,blog_id):

	blog = get_object_or_404(BlogPost,pk = blog_id)
	if blog.private and request.user.is_superuser == False:
		return HttpResponse("Not allowed to get the blog")
	
	return render(request,'blog_detail.html',{'blog':blog})

	
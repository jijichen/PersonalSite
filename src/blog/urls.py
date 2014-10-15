from django.conf.urls import patterns, include, url
from blog import views

urlpatterns = patterns('',
	url(r'^$', views.blog_list,name='blog_list'),
	url(r'^(?P<blog_id>\d+)/', views.blog_detail,name='blog_detail'),
	
	#Unfinished
	url(r'^archive/(?P<blog_year>\d+)/(?P<blog_month>\d+)/',views.blog_list,name='blog_list'),
	url(r'^archive/(?P<blog_year>\d+)/',views.blog_list,name='blog_list'),
	url(r'^cate/(?P<blog_cate>\w+)/',views.blog_list,name='blog_list'),
)
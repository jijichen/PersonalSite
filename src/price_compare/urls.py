from django.conf.urls import patterns, include, url
from price_compare import views

urlpatterns = patterns('',
	url(r'^$', views.index,name='compare_index'),
)
from django.conf.urls import patterns, include, url
from reading import views

urlpatterns = patterns('',
	url(r'^$', views.read_list,name='reading_list'),
)
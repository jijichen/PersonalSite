from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	#Administration
	url(r'^admin/', include(admin.site.urls)),
	#about
	url(r'^',include('about.urls',namespace="about")),
	url(r'^about/',include('about.urls',namespace="about")),
	#Blog
	url(r'^blog/',include('blog.urls',namespace="blog")),
	#Reading_list
	url(r'^readings/',include('reading.urls',namespace="readings")),
	#Price compare
	url(r'^compare/',include('price_compare.urls',namespace="compare")),
	#Rich text editor
	(r'^ckeditor/', include('ckeditor.urls')),
	
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

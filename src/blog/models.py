from django.conf import settings
from django.db import models
from django.utils.html import strip_tags
from pyquery import PyQuery
import cgi

#Base models for common part
class BaseModel(models.Model):
	class Meta:
		abstract = True
		app_label = 'blog'

# Real Models 
''' Category of the blogs '''
class BlogCategory(BaseModel):
	class Meta:
		verbose_name='Category'

	cate = models.CharField(max_length=100,default='Unclassified',unique=True,verbose_name='category name')
	desc = models.CharField(max_length=300,null=True,blank=True,verbose_name='description')

	def get_obsolute_url(self):
		return (reverse('blog.get_blogs',kwargs={'cate':cate}))

	def __unicode__(self):
		return self.cate

class BlogPost(models.Model):
	class Meta:
		verbose_name = 'Article'
		
	title = models.CharField(max_length=150,unique=True)
	body = models.TextField()
	category = models.ForeignKey(BlogCategory,verbose_name='Category')
	private = models.BooleanField(default=False)
	timestamp = models.DateTimeField()
	#abstract = __generate_abstract(strip_tags(body))
	cover_src = ''

	def __unicode__(self):
		return self.title

	def generate_summary(self, nchars=200):
		'''Get summay in first nchars chars'''
		orig_html = PyQuery(self.body)

		summary_text = orig_html.text()[:int(nchars)]
		return summary_text

	def get_cover(self):
		'''Get a image from the blog'''
		orig_html = PyQuery(self.body)
		cover_src = ''
		cover = orig_html('img.cover:first') or orig_html('img:first')
		if cover:
			cover_src = cover.attr('src')
			return cover_src
		return ''


class BlogComment(models.Model):
	blogpost = models.ForeignKey(BlogPost)
	email = models.EmailField()
	body = models.TextField(max_length=400)
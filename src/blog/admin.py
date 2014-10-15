from django.contrib import admin
from blog.models import *
from ckeditor.widgets import CKEditorWidget
#Administration

class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title','category','body','timestamp','private')
	formfield_overrides={models.TextField:{'widget':CKEditorWidget},}

class BlogCommentAdmin(admin.ModelAdmin):
	list_display = ('blogpost','email','body')

class BlogCateAdmin(admin.ModelAdmin):
	list_display = ('cate','desc')

admin.site.register(BlogPost,BlogPostAdmin)
admin.site.register(BlogComment,BlogCommentAdmin)
admin.site.register(BlogCategory,BlogCateAdmin)
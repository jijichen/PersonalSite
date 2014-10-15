from django.contrib import admin
from reading.models import *

#Administration for readings
class BookListAdmin(admin.ModelAdmin):
	list_display = ('title','timestamp','Author','complete','cover','cover_thumbnail')

class BookCateAdmin(admin.ModelAdmin):
	list_display = ('cate',)

admin.site.register(ReadingBooks,BookListAdmin)
admin.site.register(BookCategory,BookCateAdmin)
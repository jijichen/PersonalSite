# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from reading.models import ReadingBooks,BookCategory

from django.core.urlresolvers import reverse

#shortcuts
from django.shortcuts import render



def read_list(request):
	if request.user.is_superuser == True:
		pass
	
	cates = BookCategory.objects.all()


	book_cate_dic = {}
	for cate in cates:
		book_in_cate = ReadingBooks.objects.filter(bookcategory = cate)
		book_cate_dic[cate] = book_in_cate
	
	books = ReadingBooks.objects.all()

	return render(request,'reading_list.html',{'dict':book_cate_dic})

	
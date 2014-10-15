from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

#Validatiors 
from django.core.exceptions import ValidationError

def validator_percent(value):
	if (value > 100) or (value < 0):
		raise ValidationError("The value should between 0 to 100")

# Create your models here.

class BookCategory(models.Model):
	cate = models.CharField(max_length=100,verbose_name="Category of Books")

	def __unicode__(self):
		return self.cate

class ReadingBooks(models.Model):
	class Meta:
		verbose_name='Reading Books'

	title = models.CharField(max_length=100,verbose_name="Title of the Book")
	Author = models.CharField(max_length=50,verbose_name="Author name")
	complete = models.PositiveSmallIntegerField(validators=[validator_percent])
	cover = models.ImageField(upload_to='books_cover')
	cover_thumbnail = ImageSpecField(
			source = 'cover',
			processors=[ResizeToFill(100,50)],
			format="PNG",
			options={'quality':60}
		)
	timestamp = models.DateTimeField()
	

	#Foreign key
	bookcategory = models.ForeignKey(BookCategory,verbose_name="Category of Book")

	def __unicode__(self):
		return self.title

		




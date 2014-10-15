from django import forms

class CommentForm(forms.Form):
	guest_email = forms.EmailField(required = True,label = "Your E-mail")
	guest_comment = forms.CharField(required = True,max_length = 500,label = "Comment")
	
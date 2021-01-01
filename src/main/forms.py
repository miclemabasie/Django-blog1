from blog.models import Post
from django import forms


class ContactForm(forms.Form):
    username = forms.CharField(max_length=45, required=True)
    email = forms.EmailField(required=False)
    subject = forms.CharField(max_length=46, required=False)
    message = forms.CharField(max_length=89, required=False)

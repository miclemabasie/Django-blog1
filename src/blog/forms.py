from django import forms
from .models import Comment

# form for sharing post
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

    
    def item_description(self, item):
        return truncatewords(item.body, 30)


class SearchForm(forms.Form):
    query = forms.CharField(max_length=1024, required=True)
    
    


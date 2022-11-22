from django import forms
from .models import Posting, Comment

class PostingForm(forms.ModelForm):
    title = forms.CharField(label='제목')
    content = forms.CharField(label='내용', strip=False, widget=forms.Textarea)

    class Meta:
        model = Posting
        fields = ['title', 'content',]

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', strip=False, widget=forms.Textarea(attrs={'rows':2}))

    class Meta:
        model = Comment
        fields = ['content',]

from django import forms
from .models import Topic, Entry, Comment
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class TopicForm(forms.ModelForm):
    
    class Meta:

        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    
    text = forms.CharField(label='', widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:

        model = Entry
        fields = ['title', 'text']
        labels = {'title': ''}


class CommentForm(forms.ModelForm):
    
    class Meta:

        model = Comment
        fields = ['text']
        labels = {'text': 'Добавить комментарий'}
        widgets = {'name': forms.Textarea(attrs={'cols': 80, 'rows': 30})}
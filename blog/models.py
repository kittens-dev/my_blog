from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Topic(models.Model):

    text = models.CharField(max_length=200)

    date_added = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        
        return self.text

    class Meta:

        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Entry(models.Model):

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    text = HTMLField()

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

        def __str__(self):
            
            if len(self.text) > 50:               
                return self.text[:50] + "..."


class Comment(models.Model):

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    text = models.TextField()

    date_added = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'    
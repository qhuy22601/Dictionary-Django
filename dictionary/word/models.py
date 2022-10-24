from django.db import models


class Word(models.Model):
    raw = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')


class Sentence(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    raw = models.CharField(max_length=200)

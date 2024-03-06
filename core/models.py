from django.db import models
from . choices import *
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='profile')
    preference = models.TextField(null=True, blank=True)
    blacklist = models.TextField(null=True, blank=True)
    avatar = models.FileField(upload_to='avatar/', default='avatar/default-avatar.png')
    account_created = models.DateField(null=True, blank=True)
    

# class Book(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class Note(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True)
    book = models.ForeignKey('Library', on_delete=models.CASCADE, null=True)
    volume = models.IntegerField(null=True)
    note = models.TextField()
    reading_status = models.CharField(
        max_length=20,
        choices=READING_STATUS,
        default=TOR
    )
    current_progress = models.CharField( # For tracking how many chapter have been read
        max_length=30,
        blank=True, 
        default='not yet read'
    )
    source = models.CharField(max_length=100, default='none', blank=True) # source can refer to downloage page, example = https://www.justlightnovels.com/2023/03/hollow-regalia/

# Models containing both Books and Author, so in case User delete a book, database will still have a data about what book is authored by who. 
# This'll be useful to build a library database.
class Library(models.Model):
    profile = models.ManyToManyField(Profile)
    title = models.CharField(max_length=50, null=True)
    author = models.CharField(
        max_length=50,
        null=True
    )
    author_medsos = models.CharField(max_length=30, default='none', blank=True)
    book_type = models.CharField(
        max_length=10,
        null=True,
        choices=BOOKS_TYPES
    )
    tl_type = models.CharField(
        max_length=20,
        null=True, 
        choices=TRANSLATION_BY
    )
    series_status = models.CharField(
        max_length=20,
        choices=SERIES_STATUS,
        default=ONG
    )
    cover = models.FileField(upload_to='cover/', default='cover/default.png', blank=True)
    genre = models.CharField(max_length=100, blank=True, null=True)



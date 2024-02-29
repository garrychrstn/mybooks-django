from django.db import models
from . choices import *
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    preference = models.TextField
    blacklist = models.TextField
    avatar = models.FileField(upload_to='avatar/', default='avatar/default-avatar.png')
    account_created = models.DateField(null=True, blank=True)

class Books(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    author = models.CharField(
        max_length=40,
    )
    author_nationality = models.CharField(max_length=20, default='Japanese')
    author_medsos = models.CharField(max_length=30, default='None')
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
    source = models.CharField(max_length=100) # source can refer to downloage page, example = https://www.justlightnovels.com/2023/03/hollow-regalia/
    reading_status = models.CharField(
        max_length=20,
        choices=READING_STATUS,
        default=TOR
    )
    current_progress = models.CharField( # For tracking how many chapter have been read
        max_length=30,
        null=True
    )
    cover = models.FileField(upload_to='cover/', default='cover/default.png')
    genre = models.CharField(max_length=40, null=True)

class Notes(models.Model):
    books = models.ForeignKey('Books', on_delete=models.CASCADE, null=True)
    volume = models.IntegerField(null=True)
    note = models.TextField()

# Models containing both Books and Author, so in case User delete a book, database will still have a data about what book is authored by who. 
# This'll be useful to build a library database.
class Archive(models.Model):
    author = models.CharField(max_length=40)
    author_nationality = models.CharField(max_length=20)
    author_medsos = models.CharField(max_length=30)    
    books = models.CharField(max_length=30)





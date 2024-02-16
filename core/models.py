from django.db import models
from . choices import *
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Books(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
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
    
class Author(models.Model):
    name = models.CharField(max_length=30)
    # one-to-many relationship has been established with use of author in Books model as ForeignKey,
    natio = models.CharField(max_length = 12)
    medsos = models.CharField(max_length=100) # multiple medsos, for example ig:@garrychrstn, twitter:@garrychrstn


# Models containing both Books and Author, so in case User delete a book, database will still have a data about what book is authored by who. 
# This'll be useful to build a library database.
class Library(models.Model):
    author = models.CharField(max_length=40)
    books = models.CharField(max_length=30)






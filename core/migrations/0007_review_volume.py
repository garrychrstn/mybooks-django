# Generated by Django 4.1.7 on 2024-02-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_books_genre_alter_books_reading_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='volume',
            field=models.IntegerField(null=True),
        ),
    ]
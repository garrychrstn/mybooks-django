# Generated by Django 4.1.7 on 2024-02-17 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_archive_books_auhor_nationality_books_author_medsos_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='auhor_nationality',
            new_name='author_nationality',
        ),
        migrations.AlterField(
            model_name='books',
            name='reading_status',
            field=models.CharField(choices=[('DROP', 'DROP'), ('ON-HOLD', 'ON-HOLD'), ('FINISH', 'FINISH'), ('NOT YET READ', 'NOT YET READ'), ('TO READ', 'TO READ')], default='TO READ', max_length=20),
        ),
    ]

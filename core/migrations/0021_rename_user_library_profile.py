# Generated by Django 4.1.7 on 2024-03-02 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_library_current_progress_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='library',
            old_name='user',
            new_name='profile',
        ),
    ]

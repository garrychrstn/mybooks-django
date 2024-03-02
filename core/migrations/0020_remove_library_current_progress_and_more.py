# Generated by Django 4.1.7 on 2024-03-02 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_library_note_delete_archive_remove_notes_books_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='current_progress',
        ),
        migrations.RemoveField(
            model_name='library',
            name='reading_status',
        ),
        migrations.AddField(
            model_name='note',
            name='current_progress',
            field=models.CharField(blank=True, default='not yet read', max_length=30),
        ),
        migrations.AddField(
            model_name='note',
            name='reading_status',
            field=models.CharField(choices=[('DROP', 'DROP'), ('ON-HOLD', 'ON-HOLD'), ('FINISH', 'FINISH'), ('NOT YET READ', 'NOT YET READ'), ('TO READ', 'TO READ'), ('READING', 'READING')], default='TO READ', max_length=20),
        ),
    ]

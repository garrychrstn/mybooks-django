# Generated by Django 4.1.7 on 2024-03-09 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_note_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

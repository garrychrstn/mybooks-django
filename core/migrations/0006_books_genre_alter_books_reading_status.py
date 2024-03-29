# Generated by Django 4.1.7 on 2024-02-23 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='genre',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='reading_status',
            field=models.CharField(choices=[('DROP', 'DROP'), ('ON-HOLD', 'ON-HOLD'), ('FINISH', 'FINISH'), ('NOT YET READ', 'NOT YET READ'), ('TO READ', 'TO READ'), ('READING', 'READING')], default='TO READ', max_length=20),
        ),
    ]

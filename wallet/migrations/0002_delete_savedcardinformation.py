# Generated by Django 4.0.3 on 2022-05-06 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SavedCardInformation',
        ),
    ]
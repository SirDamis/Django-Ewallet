# Generated by Django 4.0.3 on 2022-05-06 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='be480470515342dd90c7a5b780fdb09b', editable=False, primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 4.0.3 on 2022-09-16 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_alter_wallet_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='number',
            field=models.UUIDField(default='5ad6aaf489e2480b836e2d5671a77406', editable=False, primary_key=True, serialize=False),
        ),
    ]

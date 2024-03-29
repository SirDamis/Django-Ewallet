# Generated by Django 4.0.3 on 2023-04-01 02:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0008_alter_wallet_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

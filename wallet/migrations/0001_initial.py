# Generated by Django 4.0.3 on 2022-05-06 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedCardInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=14)),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
                ('last_transaction', models.DateField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=16, unique=True)),
                ('details', models.TextField(null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('type', models.CharField(max_length=14)),
                ('success', models.BooleanField(default=False)),
                ('by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_by', to=settings.AUTH_USER_MODEL)),
                ('to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

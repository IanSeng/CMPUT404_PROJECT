# Generated by Django 3.1.6 on 2021-03-01 23:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('remote_server_url', models.URLField(primary_key=True, serialize=False, unique=True)),
                ('remote_server_username', models.CharField(blank=True, default='', max_length=200)),
                ('remote_server_password', models.CharField(blank=True, default='', max_length=200, validators=[django.core.validators.MinLengthValidator(8)])),
                ('adminApproval', models.BooleanField(default=False)),
                ('konnection_username', models.CharField(blank=True, default='', max_length=200)),
                ('konnection_password', models.CharField(blank=True, default='', max_length=200)),
            ],
        ),
    ]

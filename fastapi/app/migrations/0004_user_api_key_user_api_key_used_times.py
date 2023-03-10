# Generated by Django 4.1.5 on 2023-01-28 08:40

import secrets

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_unit_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="api_key",
            field=models.CharField(
                default=secrets.token_urlsafe, max_length=60, verbose_name="api key"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="api_key_used_times",
            field=models.IntegerField(default=0, verbose_name="api key used times"),
        ),
    ]

# Generated by Django 3.1.2 on 2020-10-06 06:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notes", "0002_auto_20201005_1736"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="notebook",
            unique_together={("user", "title")},
        ),
    ]
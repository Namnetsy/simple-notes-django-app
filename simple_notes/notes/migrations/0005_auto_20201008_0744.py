# Generated by Django 3.1.2 on 2020-10-08 07:44

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_auto_20201008_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='content',
            field=django_summernote.fields.SummernoteTextField(blank=True),
        ),
    ]
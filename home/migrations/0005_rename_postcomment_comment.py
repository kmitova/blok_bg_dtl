# Generated by Django 4.1.3 on 2022-11-29 12:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_alter_postcomment_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostComment',
            new_name='Comment',
        ),
    ]
